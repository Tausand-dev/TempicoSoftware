# -*- coding: utf-8 -*-
"""ThreadG2

    Worker thread for computing the g²(τ) second-order correlation function
    (HBT experiment) in real time from start-stop events acquired with a
    Tausand Tempico TDC device.

    The algorithm is based on the HBT histogram approach from Prueba7.py:
    a symmetric histogram of τ delays is accumulated and normalized by the
    mean of all non-zero bins (tail-normalization), yielding g²(τ) = 1 in
    the uncorrelated baseline. Color classification and "light type" labels
    are deliberately excluded.

    The thread mirrors the WorkerThreadFCS structure exactly:
    - Same five signals (dataReady, statusUpdate, colorValue, stringValue,
      threadCreated).
    - Same saveCurrentSettings / applyCurrentSettings lifecycle.
    - Same loop structure with a total_seconds finite-duration option.

    | @author: Miguelangel García Castillo, Tausand Electronics
    | mgarcia@tausand.com
    | https://www.tausand.com
"""

import sys
import time
import io

import numpy as np
from PySide2.QtCore import QThread, Signal, Slot
import pyTempico as tempico


# Overflow sentinel returned by pyTempico when no valid stop is recorded.
_OVERFLOW_SENTINEL = -1_000_000


class WorkerThreadG2(QThread):
    """
    Worker thread for g²(τ) HBT acquisition and real-time histogram update.

    Runs entirely in the background so the GUI thread stays responsive during
    the measurement. Communicates with the GUI exclusively through Qt signals.

    The thread calls ``device.measure()`` in a continuous loop and processes
    each row's stop_ps1 time into a nanosecond delay τ.  Valid τ values are
    accumulated into a symmetric histogram spanning [−window_ns, +window_ns]
    with bin width bin_ns.  After every batch the normalized g²(τ) curve is
    emitted via ``dataReady``.

    Normalization (from Prueba7.py):
        baseline = mean( counts[counts > 0] )
        g²(τ)   = counts(τ) / baseline

    Signals
    -------
    dataReady : Signal(object, object, int, float, float)
        Emitted after every ``measure()`` call with
        ``(centres_ns, g2, total_events, rate_starts, rate_stops)``.
    statusUpdate : Signal(str)
        Emitted after every ``measure()`` call with a human-readable status
        string (event count, elapsed time).
    colorValue : Signal(int)
        Status-indicator colour code: 1 = running OK, 3 = warning / no data.
    stringValue : Signal(str)
        Short status messages for the status label.
    threadCreated : Signal(int)
        Emitted with 0 when the loop starts, 1 when it stops.

    Parameters
    ----------
    parent : QWidget
        Parent widget that owns this thread.
    device : tempico.TempicoDevice
        Open Tempico device instance.
    stop_channel : int
        Which TDC channel (1–4) carries the stop signal. Default: 1.
    bin_ns : float
        Histogram bin width in nanoseconds. Default: 2.0 ns.
    window_ns : float
        Half-window in nanoseconds; histogram spans [−window_ns, +window_ns].
        Default: 200.0 ns.
    mode : int
        TDC acquisition mode (1 = ±200 ns typical, 2 = up to 4 ms). Default: 1.
    num_runs : int
        Number of runs per ``measure()`` call. Default: 100.
    channel_mode : int
        TDC mode applied to the stop channel at device configuration time.
        Kept for symmetry with WorkerThreadFCS; mirrors ``mode``. Default: 1.
    total_seconds : float or None
        If set, the loop exits after this many wall-clock seconds. If None,
        the loop runs until ``stop()`` is called. Default: None.
    """

    dataReady     = Signal(object, object, int, float, float)
    statusUpdate  = Signal(str)
    colorValue    = Signal(int)
    stringValue   = Signal(str)
    threadCreated = Signal(int)

    def __init__(
        self,
        parent,
        device: tempico.TempicoDevice,
        stop_channel: int   = 1,
        bin_ns:       float = 2.0,
        window_ns:    float = 200.0,
        total_seconds       = None,
    ):
        super().__init__()

        self.parent        = parent
        self.device        = device
        self.stop_channel  = stop_channel
        self.bin_ns        = bin_ns
        self.window_ns     = window_ns
        self.total_seconds = total_seconds

        # Loop-control sentinel; set to False by stop()
        self.itsRunning        = True
        # Consecutive device errors — auto-stop on persistent hardware fault
        self.consecutiveErrors = 0

        # ── Photon counters ───────────────────────────────────────────────────
        self.n_starts     = 0
        self.n_stops      = 0
        self.total_events = 0

        # ── Build symmetric histogram [-window_ns, +window_ns] ───────────────
        # Edges are offset by half a bin so bin centres fall exactly on
        # 0, ±bin_ns, ±2·bin_ns, …  (always a bin centred at τ = 0).
        # n_half bins on each side → 2*n_half bins total → 2*n_half+1 edges.
        n_half   = max(int(np.ceil(window_ns / bin_ns)), 1)
        half_bin = bin_ns / 2.0
        # Left edge of bin 0 … right edge of bin 2*n_half-1
        edges = np.arange(-n_half, n_half + 1, dtype=np.float64) * bin_ns - half_bin
        # 'edges' already has 2*n_half+1 elements — no extra np.append needed.
        self.edges   = edges
        self.n_bins  = len(self.edges) - 1
        self.centres = 0.5 * (self.edges[:-1] + self.edges[1:])
        self.counts  = np.zeros(self.n_bins, dtype=np.float64)

        # isBatched and num_runs are determined in run() after reading the device
        self.isBatched = False
        self.num_runs  = 100   # placeholder; overwritten in run()

    # ── Device configuration snapshot ────────────────────────────────────────

    def saveCurrentSettings(self):
        """
        Snapshot the current device configuration.

        Stores all relevant channel and global parameters so they can be
        re-applied with ``applyCurrentSettings()`` after the thread finishes.
        Mirrors ``WorkerThreadFCS.saveCurrentSettings``.

        :return: None
        """
        self.numberRunsSetting    = self.device.getNumberOfRuns()
        self.thresholdVoltage     = self.device.getThresholdVoltage()

        self.modeChannelA         = self.device.ch1.getMode()
        self.numberStopsChannelA  = self.device.ch1.getNumberOfStops()
        self.stopEdgeTypeChannelA = self.device.ch1.getStopEdge()
        self.stopMaskChannelA     = self.device.ch1.getStopMask()

        self.modeChannelB         = self.device.ch2.getMode()
        self.numberStopsChannelB  = self.device.ch2.getNumberOfStops()
        self.stopEdgeTypeChannelB = self.device.ch2.getStopEdge()
        self.stopMaskChannelB     = self.device.ch2.getStopMask()

        self.modeChannelC         = self.device.ch3.getMode()
        self.numberStopsChannelC  = self.device.ch3.getNumberOfStops()
        self.stopEdgeTypeChannelC = self.device.ch3.getStopEdge()
        self.stopMaskChannelC     = self.device.ch3.getStopMask()

        self.modeChannelD         = self.device.ch4.getMode()
        self.numberStopsChannelD  = self.device.ch4.getNumberOfStops()
        self.stopEdgeTypeChannelD = self.device.ch4.getStopEdge()
        self.stopMaskChannelD     = self.device.ch4.getStopMask()

    def applyCurrentSettings(self):
        """
        Re-apply the snapshotted device configuration.

        Called after the acquisition loop exits to restore the device to the
        state it was in before the G2 measurement started.
        Mirrors ``WorkerThreadFCS.applyCurrentSettings``.

        :return: None
        """
        self.device.setNumberOfRuns(self.numberRunsSetting)
        self.device.setThresholdVoltage(self.thresholdVoltage)

        self.device.ch1.setMode(self.modeChannelA)
        self.device.ch1.setNumberOfStops(self.numberStopsChannelA)
        self.device.ch1.setStopEdge(self.stopEdgeTypeChannelA)
        self.device.ch1.setStopMask(self.stopMaskChannelA)

        self.device.ch2.setMode(self.modeChannelB)
        self.device.ch2.setNumberOfStops(self.numberStopsChannelB)
        self.device.ch2.setStopEdge(self.stopEdgeTypeChannelB)
        self.device.ch2.setStopMask(self.stopMaskChannelB)

        self.device.ch3.setMode(self.modeChannelC)
        self.device.ch3.setNumberOfStops(self.numberStopsChannelC)
        self.device.ch3.setStopEdge(self.stopEdgeTypeChannelC)
        self.device.ch3.setStopMask(self.stopMaskChannelC)

        self.device.ch4.setMode(self.modeChannelD)
        self.device.ch4.setNumberOfStops(self.numberStopsChannelD)
        self.device.ch4.setStopEdge(self.stopEdgeTypeChannelD)
        self.device.ch4.setStopMask(self.stopMaskChannelD)

        # Re-enable all channels after the single-channel HBT configuration
        self.device.ch1.enableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        """
        Acquisition loop for g²(τ) HBT measurement.  Runs in a separate QThread.

        Configures the selected stop channel for HBT (mode, 1 stop, stop_mask
        = −0.25 µs to capture negative delays), then enters a loop that calls
        ``device.measure()`` until ``stop()`` is called or ``total_seconds``
        have elapsed.  Each batch accumulates τ values into the symmetric
        histogram, recomputes g²(τ), and emits the updated curve.

        :return: None
        """
        self.threadCreated.emit(0)

        # ── Snapshot device settings as the very first thing in run() ─────────
        # Doing this here (not in __init__) guarantees that no device API call
        # can throw a silent exception that kills the Qt slot before the thread
        # even starts — exactly the pattern WorkerThreadFCS follows.
        self.saveCurrentSettings()

        # Read the currently configured number of runs and decide batching
        self.num_runs  = self.numberRunsSetting
        self.isBatched = (self.num_runs > 50)

        # HBT always uses TDC Mode 1 (≈±200 ns range); no user selection needed.
        _mode = 1

        # ── Save generator settings for TP12 (reset clears them) ─────────────
        is_tp12 = "TP12" in self.device.getModelIdn()
        if is_tp12:
            saved_gen_freq   = self.device.getGeneratorFrequency()
            saved_start_srcs = [self.device.getStartSource(ch) for ch in [1, 2, 3, 4]]
            saved_stop_srcs  = [self.device.getStopSource(ch)  for ch in [1, 2, 3, 4]]

        # Reset clears previous measurements and default-restores settings
        self.device.reset()

        # Restore generator settings if TP12
        if is_tp12:
            if saved_gen_freq:
                self.device.setGeneratorFrequency(saved_gen_freq)
            for idx, ch_num in enumerate([1, 2, 3, 4]):
                if saved_start_srcs[idx] == "INTERNAL":
                    self.device.setStartInternalSource(ch_num)
                else:
                    self.device.setStartExternalSource(ch_num)
                if saved_stop_srcs[idx] == "INTERNAL":
                    self.device.setStopInternalSource(ch_num)
                else:
                    self.device.setStopExternalSource(ch_num)

        # Restore threshold voltage
        self.device.setThresholdVoltage(self.thresholdVoltage)

        # ── Disable all channels, then enable only the stop channel ───────────
        _all_chs = [self.device.ch1, self.device.ch2,
                    self.device.ch3, self.device.ch4]
        for ch in _all_chs:
            ch.disableChannel()

        _stop_edges = [
            self.stopEdgeTypeChannelA, self.stopEdgeTypeChannelB,
            self.stopEdgeTypeChannelC, self.stopEdgeTypeChannelD,
        ]

        self._active_ch = _all_chs[self.stop_channel - 1]
        self._active_ch.enableChannel()
        self._active_ch.setMode(_mode)
        self._active_ch.setNumberOfStops(1)
        # Stop mask = −0.25 µs: allows the TP1204 to capture negative delays natively
        self._active_ch.setStopMask(-0.25)
        self._active_ch.setAverageCycles(1)
        active_stop_edge = _stop_edges[self.stop_channel - 1]
        self._active_ch.setStopEdge(active_stop_edge)

        self.device.setNumberOfRuns(self.num_runs)

        call_count = 0
        t_start    = time.time()

        # ── Acquisition loop ───────────────────────────────────────────────
        while self.itsRunning:
            if self.total_seconds is not None:
                elapsed = time.time() - t_start
                if elapsed >= self.total_seconds:
                    break
                if call_count > 0:
                    t_per_run   = elapsed / call_count
                    time_left   = self.total_seconds - elapsed
                    runs_to_use = max(1, int(time_left / t_per_run))
                    runs_to_use = min(runs_to_use, self.num_runs)
                    self.device.setNumberOfRuns(runs_to_use)

            call_count = self._getMeasurements(call_count, t_start)

        # Restore device configuration and signal completion
        self.applyCurrentSettings()
        self.stringValue.emit("G2 acquisition finished.")
        self.colorValue.emit(1)
        self.threadCreated.emit(1)

    # ── Batch measurement step ────────────────────────────────────────────────

    def _getMeasurements(self, call_count: int, t_start: float) -> int:
        """
        Acquire one batch from the device, accumulate τ into the histogram,
        recompute g²(τ), and emit all relevant signals.

        Mirrors ``WorkerThreadFCS._getMeasurements`` in structure.

        :param call_count: Number of ``measure()`` calls completed so far.
        :param t_start: Wall-clock timestamp at acquisition start (seconds).
        :return: Updated call_count.
        """
        try:
            # Suppress pyTempico console output (same pattern as Prueba7.py)
            _orig_stdout = sys.stdout
            sys.stdout   = io.StringIO()
            data         = self.device.measure()
            sys.stdout   = _orig_stdout

            if not data:
                self.colorValue.emit(3)
                self.stringValue.emit("No measurements in channel: Start")
                self.consecutiveErrors = 0
                return call_count

            overflow_val = self.device.getOverflowParameter()

            # Check whether all stops on the active channel are missing
            all_missing = all(
                all(t == -1 or t == overflow_val for t in row[3:])
                for row in data
                if len(row) > 3
            )
            if all_missing:
                self.colorValue.emit(3)
                self.stringValue.emit(
                    f"No measurements in stop channel {self.stop_channel}"
                )
                self.consecutiveErrors = 0
                return call_count

            taus_batch_ns = []

            for run_row in data:
                if not run_row:
                    # Empty row → no START in this run
                    continue

                ch = run_row[0]
                if ch != self.stop_channel:
                    continue          # Only the selected stop channel

                # Number of valid stops in this row (HBT uses exactly 1 stop)
                n_stops_row = self._getRange(run_row, 1)
                for i in range(n_stops_row):
                    raw_ps = run_row[3 + i]

                    # Discard overflow / sentinel
                    if raw_ps == overflow_val or raw_ps == -1:
                        continue

                    self.n_starts += 1

                    # Convert ps → ns (sign preserved — TP1204 can give τ < 0)
                    tau_ns = raw_ps / 1_000.0

                    self.n_stops      += 1
                    self.total_events += 1

                    if self.isBatched:
                        taus_batch_ns.append(tau_ns)
                    else:
                        self._accumulate([tau_ns])

            # Flush the batch
            if self.isBatched and taus_batch_ns:
                self._accumulate(taus_batch_ns)

            call_count += 1

            # Recompute g²(τ) and emit
            elapsed = time.time() - t_start
            g2, rate_s, rate_p, baseline = self._compute_g2(elapsed)

            self.dataReady.emit(
                self.centres, g2, self.total_events, rate_s, rate_p
            )

            # Status string (same format as FCS so G2Logic can reuse parser)
            if self.total_seconds is not None:
                status_str = (
                    f"events: {self.total_events} | "
                    f"elapsed: {elapsed:.1f} s / {self.total_seconds} s"
                )
            else:
                status_str = (
                    f"events: {self.total_events} | "
                    f"elapsed: {elapsed:.1f} s"
                )

            if self.total_events == 0:
                self.colorValue.emit(3)
                self.stringValue.emit(
                    f"No measurements in stop channel {self.stop_channel}"
                )
            else:
                self.colorValue.emit(1)
                self.stringValue.emit(status_str)
                self.statusUpdate.emit(status_str)

            self.consecutiveErrors = 0

        except Exception as e:
            # Restore stdout if it was intercepted when the exception occurred
            try:
                sys.stdout = sys.__stdout__
            except Exception:
                pass
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors += 1
            if self.consecutiveErrors > 10:
                self.stop()

        return call_count

    # ── Histogram helpers (ported from Prueba7.py HBTWorker) ─────────────────

    def _accumulate(self, taus_ns):
        """
        Accumulate a list of τ values [ns] into the histogram.

        Only values that fall inside the pre-computed edges are counted.
        Uses np.digitize for robust bin assignment consistent with self.edges.

        :param taus_ns: Iterable of delay values in nanoseconds.
        :return: None
        """
        arr = np.asarray(taus_ns, dtype=np.float64)
        # Keep only values strictly inside the histogram range
        lo = self.edges[0]
        hi = self.edges[-1]
        valid = (arr >= lo) & (arr < hi)
        arr = arr[valid]
        if len(arr) == 0:
            return
        # np.digitize returns 1-based bin indices; subtract 1 for 0-based
        idx = np.digitize(arr, self.edges) - 1
        idx = np.clip(idx, 0, self.n_bins - 1)
        np.add.at(self.counts, idx, 1)

    def _compute_g2(self, t_elapsed: float):
        """
        Normalize the accumulated histogram to produce g²(τ).

        Normalization (tail method, Prueba7.py):
            baseline = mean( counts[counts > 0] )
            g²(τ)   = counts(τ) / baseline

        This is correct for a single-TDC start→stop measurement where
        n_stops ≈ n_starts and the classical ``r·r·T·Δt`` formula would
        produce a vanishingly small baseline.

        Also computes start and stop rates for display.

        :param t_elapsed: Wall-clock seconds since acquisition began.
        :return: Tuple (g2, rate_starts, rate_stops, baseline).
        """
        g2     = np.zeros(self.n_bins, dtype=np.float64)
        rate_s = self.n_starts / t_elapsed if t_elapsed > 0 else 0.0
        rate_p = self.n_stops  / t_elapsed if t_elapsed > 0 else 0.0

        if self.n_stops < 10:
            return g2, rate_s, rate_p, 0.0

        # Baseline = mean of all non-empty bins
        all_nonzero = self.counts[self.counts > 0]
        if len(all_nonzero) >= 2:
            baseline = float(np.mean(all_nonzero))
        else:
            baseline = 1.0

        if baseline > 0:
            g2 = self.counts / baseline

        return g2, rate_s, rate_p, baseline

    def _getRange(self, run_row, stop_number: int) -> int:
        """
        Return the number of valid stop values in a measurement row.

        Mirrors the ``getRange`` helper from Prueba7.py / ThreadStartStop.

        :param run_row: A single measurement row from pyTempico.
        :param stop_number: Maximum number of stops to expect.
        :return: Number of valid stop slots in the row.
        """
        total_len = len(run_row)
        if total_len >= 4:
            return min(total_len - 3, stop_number)
        return 0

    # ── Public control interface ──────────────────────────────────────────────

    @Slot()
    def stop(self):
        """
        Request the acquisition loop to exit on the next iteration.

        Sets ``itsRunning`` to False and emits ``threadCreated(1)`` to notify
        the GUI that the thread is stopping.

        :return: None
        """
        self.threadCreated.emit(1)
        self.itsRunning = False