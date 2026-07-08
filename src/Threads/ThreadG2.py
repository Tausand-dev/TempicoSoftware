# -*- coding: utf-8 -*-

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

    Rate (stop-stop):
        The displayed rate is NOT total_events / elapsed_time — that naive
        estimate is skewed by the hardware dead-time between acquisition
        runs. Instead, the stop channel is configured for exactly the
        number of stops per run requested by the caller (``num_stops``,
        no forced minimum), and, within each individual run, the delta
        between consecutive valid stops is accumulated (mirroring
        ``WorkerThreadFCS``'s inter-stop delta logic). The gap between the
        last stop of one run and the first stop of the next run is never
        computed, so the inter-run dead-time can't contaminate the
        estimate. The rate is then::

            Rate (stop-stop) = 1 / mean(delta_stop)

        with a guard against delta_stop <= 0 to avoid a division by zero.
        If ``num_stops`` is 1, no intra-run delta ever exists, so
        Rate (stop-stop) has no data and the UI shows it as unavailable —
        the g²(τ) histogram itself is unaffected either way, since it only
        ever uses the first stop of each run.

    Signals
    -------
    dataReady : Signal(object, object, int, float)
        Emitted after every ``measure()`` call with
        ``(centres_ns, g2, total_events, rate_stop_stop)``.
    statusUpdate : Signal(str)
        Emitted after every ``measure()`` call with a human-readable status
        string (event count, elapsed time).
    colorValue : Signal(int)
        Status-indicator colour code: 1 = running OK, 3 = warning / no data.
    stringValue : Signal(str)
        Short status messages for the status label.
    threadCreated : Signal(int)
        Emitted with 0 when the loop starts, 1 when it stops.

    Attributes
    ----------
    raw_stop_ps : list
        Every individual valid stop time recorded during the acquisition,
        in picoseconds and in arrival order. This is the raw start-stop
        data behind the accumulated g²(τ) histogram, kept so it can be
        exported separately (e.g. as ``..._StartStopTimes``).

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
    num_stops : int
        Number of stops requested per run on the active channel, exactly
        as configured by the caller (no forced minimum; 1 is the hardware
        floor). Only the first valid stop of each run is used to build the
        g²(τ) histogram regardless of this value. If less than 2, no
        intra-run stop-to-stop delta can be computed, so Rate (stop-stop)
        has no data to show. Default: 2.
    channel_mode : int
        TDC mode applied to the stop channel at device configuration time.
        Kept for symmetry with WorkerThreadFCS; mirrors ``mode``. Default: 1.
    total_seconds : float or None
        If set, the loop exits after this many wall-clock seconds. If None,
        the loop runs until ``stop()`` is called. Default: None.
    """

    dataReady     = Signal(object, object, int, float)
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
        num_stops:    int   = 2,
        total_seconds       = None,
    ):
        """
        Configures the acquisition parameters and builds the τ histogram.

        Stores the device and acquisition settings, initializes the
        loop-control and error-tracking sentinels, resets the photon
        counters, and builds the symmetric τ histogram spanning
        ``[-window_ns, +window_ns]`` with bin width ``bin_ns``. Bin edges are
        offset by half a bin so that bin centres always fall exactly on
        ``0, ±bin_ns, ±2*bin_ns, ...``, guaranteeing a bin centred at τ = 0.

        :param parent: Parent widget that owns this thread.
        :param device: Open ``tempico.TempicoDevice`` instance.
        :param stop_channel: TDC channel (1-4) carrying the stop signal.
        :type stop_channel: int
        :param bin_ns: Histogram bin width, in nanoseconds.
        :type bin_ns: float
        :param window_ns: Half-window, in nanoseconds; the histogram spans
            ``[-window_ns, +window_ns]``.
        :type window_ns: float
        :param num_stops: Number of stops requested per run on the active
            channel, exactly as configured by the user (e.g. via the
            Channels settings dialog). If 1, the g²(τ) histogram still
            works normally, but the Rate (stop-stop) display will have no
            data to show, since it needs at least 2 stops in the same run
            to compute an intra-run delta.
        :type num_stops: int
        :param total_seconds: Duration, in seconds, after which the
            acquisition loop exits automatically, or ``None`` to run until
            ``stop()`` is called.
        :return: None
        """
        super().__init__()

        self.parent        = parent
        self.device        = device
        self.stop_channel  = stop_channel
        self.bin_ns        = bin_ns
        self.window_ns     = window_ns
        # Respect exactly what was requested (no silent minimum). If the
        # caller passes 1, the active channel genuinely runs with 1 stop
        # per run: the g²(τ) histogram is unaffected (it only ever uses
        # the first stop), but no intra-run stop-to-stop delta will exist,
        # so Rate (stop-stop) will show as unavailable — see the
        # len(valid_stops) >= 2 guard further down.
        self.num_stops     = max(num_stops, 1)   # 1 is the hardware minimum
        self.total_seconds = total_seconds

        # Loop-control sentinel; set to False by stop()
        self.itsRunning        = True
        # Consecutive device errors — auto-stop on persistent hardware fault
        self.consecutiveErrors = 0

        # ── Photon counters ───────────────────────────────────────────────────
        self.n_starts     = 0
        self.n_stops      = 0
        self.total_events = 0

        # ── Raw start-stop data ───────────────────────────────────────────────
        # Every individual valid stop time (ps), in the order it was recorded,
        # kept for the whole acquisition so it can be exported as raw
        # start-stop data (independent from the accumulated g²(τ) histogram).
        self.raw_stop_ps = []

        # ── Stop-to-stop deltas (Rate stop-stop) ──────────────────────────────
        # Running accumulators for the dead-time-safe stop-stop rate: only
        # deltas between consecutive valid stops WITHIN the same run are
        # ever added here (see _getMeasurements), so the hardware dead-time
        # between runs never contaminates the estimate.
        self._sum_delta_stop_ps = 0.0
        self._n_delta_stop      = 0

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
        # Use exactly the number of stops the user configured for this
        # channel. The first stop is still the only one used to build the
        # g²(τ) histogram; if 2+ stops are requested, the extra stop(s)
        # let us compute a genuine intra-run stop-to-stop delta for the
        # Rate (stop-stop) display, free of inter-run hardware dead-time.
        # If only 1 stop is configured, Rate (stop-stop) has no data to
        # show and the UI falls back to "—" (see the len(valid_stops) >= 2
        # guard below).
        self._active_ch.setNumberOfStops(self.num_stops)
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

                # Number of valid stop slots present in this row. The active
                # channel is configured for self.num_stops (>= 2) so that,
                # when available, a second (or later) stop lets us compute a
                # genuine intra-run stop-to-stop delta.
                n_stops_row = self._getRange(run_row, self.num_stops)

                valid_stops = []
                for i in range(n_stops_row):
                    raw_ps = run_row[3 + i]
                    # Discard overflow / sentinel
                    if raw_ps == overflow_val or raw_ps == -1:
                        continue
                    valid_stops.append(raw_ps)

                if not valid_stops:
                    continue

                # ── g²(τ) histogram: only the FIRST valid stop of the run ──
                # is used — exactly as before — since it's the start→stop
                # delay the correlation histogram is built from. Any extra
                # stops are used below only for the stop-stop rate, never
                # added to the histogram.
                raw_ps0 = valid_stops[0]

                self.n_starts += 1

                # Convert ps → ns (sign preserved — TP1204 can give τ < 0)
                tau_ns = raw_ps0 / 1_000.0

                self.n_stops      += 1
                self.total_events += 1

                # Keep the raw (unbinned) stop time for later export as
                # raw start-stop data
                self.raw_stop_ps.append(raw_ps0)

                if self.isBatched:
                    taus_batch_ns.append(tau_ns)
                else:
                    self._accumulate([tau_ns])

                # ── Stop-to-stop deltas (Rate stop-stop) ────────────────────
                # Only intra-run consecutive deltas are used (mirrors
                # WorkerThreadFCS): the gap between the last stop of this run
                # and the first stop of the NEXT run includes the hardware
                # dead-time between runs and is never computed here, so it
                # can't corrupt the rate estimate.
                if len(valid_stops) >= 2:
                    prev_t = valid_stops[0]
                    for t_ps in valid_stops[1:]:
                        delta_t_ps = t_ps - prev_t
                        # Filter: discard non-positive deltas (dead-time /
                        # ordering artifacts) so they can't corrupt the mean
                        # or cause a division by zero downstream.
                        if delta_t_ps > 0:
                            self._sum_delta_stop_ps += delta_t_ps
                            self._n_delta_stop      += 1
                        prev_t = t_ps

            # Flush the batch
            if self.isBatched and taus_batch_ns:
                self._accumulate(taus_batch_ns)

            call_count += 1

            # Recompute g²(τ) and emit
            elapsed = time.time() - t_start
            g2, rate_stop_stop, baseline = self._compute_g2(elapsed)

            self.dataReady.emit(
                self.centres, g2, self.total_events, rate_stop_stop
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

        Also computes the Rate (stop-stop) for display: 1 / mean(delta_stop),
        where delta_stop is the mean of every intra-run stop-to-stop delta
        accumulated so far (see ``_getMeasurements``). Using elapsed time
        would be biased by the hardware dead-time between runs, so the rate
        is derived purely from the accumulated deltas instead.

        :param t_elapsed: Wall-clock seconds since acquisition began.
        :return: Tuple (g2, rate_stop_stop, baseline).
        """
        g2 = np.zeros(self.n_bins, dtype=np.float64)

        # Rate (stop-stop) = 1 / mean(delta_stop), guarded against
        # delta_stop == 0 (division by zero) or no valid deltas yet.
        if self._n_delta_stop > 0:
            mean_delta_stop_ps = self._sum_delta_stop_ps / self._n_delta_stop
            mean_delta_stop_s  = mean_delta_stop_ps * 1e-12   # ps → s
            rate_stop_stop = (1.0 / mean_delta_stop_s) if mean_delta_stop_s != 0 else 0.0
        else:
            rate_stop_stop = 0.0

        if self.n_stops < 10:
            return g2, rate_stop_stop, 0.0

        # Baseline = mean of all non-empty bins
        all_nonzero = self.counts[self.counts > 0]
        if len(all_nonzero) >= 2:
            baseline = float(np.mean(all_nonzero))
        else:
            baseline = 1.0

        if baseline > 0:
            g2 = self.counts / baseline

        return g2, rate_stop_stop, baseline

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