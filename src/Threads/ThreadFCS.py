# -*- coding: utf-8 -*-
"""ThreadFCS

    Worker thread for computing the normalized autocorrelation function G(tau)
    in real time from photon arrival times acquired with a Tausand Tempico TDC
    device. Runs the multi-tau algorithm entirely in background so the GUI
    thread stays responsive during acquisition.

    The ``MultiTauCorrelator`` class is embedded directly in this module: it
    is an internal implementation detail of the thread and is not exported.

    | @author: Miguelangel García Castillo, Tausand Electronics
    | mgarcia@tausand.com
    | https://www.tausand.com
"""

from PySide2.QtCore import QThread, Signal, Slot
import numpy as np
import time
import pyTempico as tempico


# ─────────────────────────────────────────────────────────────────────────────
# Internal helper – Multi-tau autocorrelator
# ─────────────────────────────────────────────────────────────────────────────

class _MultiTauCorrelator:
    """
    Multi-tau autocorrelation algorithm for Fluorescence Correlation
    Spectroscopy (FCS).

    Computes the normalized autocorrelation function G(tau) from a stream of
    intensity values (photon counts per bin) using the multi-tau scheme, which
    combines linear spacing at short lag times with logarithmic spacing at long
    lag times.

    The normalization used is:

        G(tau) = <I(t) * I(t + tau)> / <I(t)>^2

    Parameters
    ----------
    tau_0 : float
        Base lag time (duration of the smallest bin) in picoseconds.
    num_levels : int
        Number of levels in the multi-tau hierarchy.
    m : int
        Number of channels (shift-register length) per level. Must be a
        positive even integer.
    """

    def __init__(self, tau_0=1_000_000, num_levels=16, m=16):
        self.tau_0      = tau_0
        self.num_levels = num_levels
        self.m          = m

        # One circular shift register per level
        self.shift_registers = [np.zeros(m) for _ in range(num_levels)]
        # Accumulated cross-products (numerator of G)
        self.A               = [np.zeros(m) for _ in range(num_levels)]
        # Accumulated delayed values (denominator term)
        self.M_del           = [np.zeros(m) for _ in range(num_levels)]
        # Accumulated direct values (denominator term)
        self.M_dir           = np.zeros(num_levels)
        # Number of bins processed at each level
        self.n_bins          = np.zeros(num_levels, dtype=int)
        # Buffer for coarsening pairs of bins between levels
        self.z_buffer        = np.zeros(num_levels)

    def reset(self):
        """Reset all accumulators to zero (clears the correlation history)."""
        for k in range(self.num_levels):
            self.shift_registers[k][:] = 0.0
            self.A[k][:]               = 0.0
            self.M_del[k][:]           = 0.0
        self.M_dir[:]   = 0.0
        self.n_bins[:]  = 0
        self.z_buffer[:] = 0.0

    def process_datum(self, value):
        """
        Feed a single intensity bin into the correlator.

        Parameters
        ----------
        value : float
            Photon count for the current time bin of duration ``tau_0``.
        """
        self._run_level(0, value)

    def _run_level(self, k, z_k):
        """Recursive multi-tau update at level k with input value z_k."""
        self.A[k]     += z_k * self.shift_registers[k]
        self.M_del[k] += self.shift_registers[k]
        self.M_dir[k] += z_k
        self.n_bins[k] += 1

        self.shift_registers[k]    = np.roll(self.shift_registers[k], 1)
        self.shift_registers[k][0] = z_k

        if k + 1 < self.num_levels:
            self.z_buffer[k + 1] += z_k
            if self.n_bins[k] % 2 == 0:
                new_z                = self.z_buffer[k + 1]
                self.z_buffer[k + 1] = 0.0
                self._run_level(k + 1, new_z)

    def get_correlation_curve(self):
        """
        Compute and return the normalized autocorrelation function G(tau).

        Returns
        -------
        taus : numpy.ndarray
            Lag times in the same units as ``tau_0`` (picoseconds).
        g_vals : numpy.ndarray
            Normalized autocorrelation values G(tau).
        """
        taus, g_vals = [], []

        for k in range(self.num_levels):
            if self.n_bins[k] < self.m:
                continue

            # Level 0: all m channels.  Level k≥1: upper m//2 channels only
            # (lower half already covered by the previous finer level).
            start_idx = 0 if k == 0 else self.m // 2

            for i in range(start_idx, self.m):
                m_del = self.M_del[k][i]
                if m_del == 0:
                    continue

                g   = (self.A[k][i] * self.n_bins[k]) / (self.M_dir[k] * m_del)
                tau = (i + 1) * (2 ** k) * self.tau_0

                taus.append(tau)
                g_vals.append(g)

        return np.array(taus), np.array(g_vals)


# ─────────────────────────────────────────────────────────────────────────────
# Worker thread
# ─────────────────────────────────────────────────────────────────────────────

class WorkerThreadFCS(QThread):
    """
    Worker thread for FCS acquisition and real-time multi-tau correlation.

    Runs entirely in the background so the GUI thread stays responsive during
    the measurement. Communicates with the GUI exclusively through Qt signals.

    The thread calls ``device.measure()`` in a continuous loop, reconstructs a
    relative photon-arrival timeline (Option B: cursor advances by the last
    stop of each run, inter-run gaps are ignored), bins the arrivals into
    intensity bins of width ``tau_0``, and feeds each bin into a
    ``_MultiTauCorrelator`` instance. The updated G(tau) curve is emitted after
    every ``measure()`` call.

    Signals
    -------
    dataReady : Signal(object, object, object)
        Emitted after every ``measure()`` call with ``(taus_ps, g, stop_times_ps)``
        arrays. Lag times and stop times are in picoseconds.
    statusUpdate : Signal(str)
        Emitted after every ``measure()`` call with a human-readable status
        string (call count, event count, elapsed time).
    colorValue : Signal(int)
        Emitted to set the status-indicator colour in the GUI.
        1 = running OK, 3 = warning / no measurement.
    stringValue : Signal(str)
        Emitted with short status messages for the status bar.
    threadCreated : Signal(int)
        Emitted with 0 when the loop starts, 1 when it stops.

    Parameters
    ----------
    parent : QWidget
        Parent widget that owns this thread.
    device : tempico.TempicoDevice
        Open Tempico device instance.
    tau_0 : int
        Base bin size in picoseconds. Default: 1 000 000 ps (1 µs).
    num_levels : int
        Number of levels in the multi-tau hierarchy. Default: 16.
    m : int
        Channels per level. Default: 16.
    """

    dataReady     = Signal(object, object, object)  # (taus_ps, g, stop_times_ps)
    statusUpdate = Signal(str)
    colorValue   = Signal(int)
    stringValue  = Signal(str)
    threadCreated = Signal(int)

    def __init__(self, parent, device: tempico.TempicoDevice,
                 stop_channel=1, start_channel=None,
                 num_runs=100, num_stops=2, channel_mode=2,
                 tau_0=1_000_000, num_levels=16,
                 m=16, total_seconds=None):
        super().__init__()

        self.parent        = parent
        self.device        = device
        self.start_channel = start_channel
        self.stop_channel  = stop_channel
        self.num_runs      = num_runs
        self.num_stops     = max(num_stops, 2)   # FCS needs at least 2 stops
        self.channel_mode  = channel_mode
        self.tau_0         = tau_0
        self.num_levels    = num_levels
        self.m             = m
        # None means run indefinitely until stop() is called
        self.total_seconds = total_seconds

        # Loop-control sentinel; set to False by stop()
        self.itsRunning = True

        # Consecutive device errors – used to auto-stop on hardware fault
        self.consecutiveErrors = 0

        # Save the device configuration that was active when the thread was
        # created so it can be restored on stop (mirrors ThreadStartStop)
        self.saveCurrentSettings()

    # ── Device configuration snapshot ────────────────────────────────────────

    def saveCurrentSettings(self):
        """
        Snapshot the current device configuration.

        Stores all relevant channel and global parameters so they can be
        re-applied with ``applyCurrentSettings()`` after the thread finishes.

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
        state it was in before the FCS measurement started.

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

        self.device.ch1.enableChannel()
        self.device.ch2.disableChannel()
        self.device.ch3.disableChannel()
        self.device.ch4.disableChannel()

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        """
        Acquisition and correlation loop. Runs in a separate QThread.

        Configures Channel 1 for FCS (mode 2, 1 stop), then enters a loop
        that calls ``device.measure()`` until ``stop()`` is called. Each batch
        of rows is processed into intensity bins and fed into the correlator.
        The updated G(tau) curve is emitted after every batch.

        :return: None
        """
        self.threadCreated.emit(0)

        # ── FCS-specific device configuration ──────────────────────────────
        # Mirrors fcsExample.py exactly:
        #   device.reset()
        #   device.ch1.enableChannel()  / ch2-4 disable
        #   device.ch1.setMode(2)
        #   device.ch1.setNumberOfStops(NUMBER_OF_STOPS=2)
        #   device.setNumberOfRuns(NUMBER_OF_RUNS=100)

        # Reset clears all previous measurements and restores default settings,
        # ensuring no leftover configuration from other tabs interferes.
        self.device.reset()

        # Enable only the selected stop channel
        _all_chs = [self.device.ch1, self.device.ch2,
                    self.device.ch3, self.device.ch4]
        for ch in _all_chs:
            ch.disableChannel()

        # Enable start channel if selected
        if self.start_channel is not None:
            self._start_ch = _all_chs[self.start_channel - 1]
            self._start_ch.enableChannel()
            self._start_ch.setMode(self.channel_mode)
            self._start_ch.setNumberOfStops(1)
        else:
            self._start_ch = None

        # Enable stop channel
        self._active_ch = _all_chs[self.stop_channel - 1]
        self._active_ch.enableChannel()
        self._active_ch.setMode(self.channel_mode)
        self._active_ch.setNumberOfStops(self.num_stops)
        self.device.setNumberOfRuns(self.num_runs)

        # ── Correlator and timeline state ──────────────────────────────────
        correlator = _MultiTauCorrelator(
            tau_0      = self.tau_0,
            num_levels = self.num_levels,
            m          = self.m,
        )

        # cursor_ps: running position on the relative timeline (ps).
        # Advances by the last stop of each run; inter-run gaps are ignored.
        cursor_ps      = 0
        # Upper edge of the current open intensity bin (ps)
        next_bin_edge  = self.tau_0
        # Photon counter for the current open bin
        photons_in_bin = 0

        call_count   = 0   # Number of measure() calls completed
        total_events = 0   # Total photon events collected so far

        # Accumulates every raw stop time (ps) received from the device.
        # Grows throughout the measurement and is emitted alongside the ACF
        # so FCSLogic can save it to disk.
        stop_times_ps = []

        t_start = time.time()   # Wall-clock time at acquisition start

        # ── Acquisition loop ───────────────────────────────────────────────
        # Runs until stop() is called (indefinite) or until total_seconds
        # have elapsed (when a finite duration was configured).
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
            (cursor_ps, next_bin_edge, photons_in_bin,
             call_count, total_events, stop_times_ps) = self._getMeasurements(
                correlator,
                cursor_ps, next_bin_edge, photons_in_bin,
                call_count, total_events,
                t_start, stop_times_ps,
            )

        # ── Flush the last partial bin ─────────────────────────────────────
        correlator.process_datum(photons_in_bin)
        taus, g = correlator.get_correlation_curve()
        if len(taus) > 0:
            self.dataReady.emit(taus, g, np.array(stop_times_ps))

        # Restore device configuration
        self.applyCurrentSettings()
        self.stringValue.emit("FCS acquisition finished.")
        self.colorValue.emit(1)
        self.threadCreated.emit(1)

    def _getMeasurements(self, correlator, cursor_ps, next_bin_edge,
                     photons_in_bin, call_count, total_events,
                     t_start, stop_times_ps):

        try:
            data = self.device.measure()

            if not data:
                self.colorValue.emit(3)
                self.stringValue.emit("No measurements in channels:  Start")
                self.consecutiveErrors = 0
                return cursor_ps, next_bin_edge, photons_in_bin, call_count, total_events, stop_times_ps

            # Check whether every stop value is -1 (stop channel silent)
            all_stops_missing = all(
                all(t == -1 for t in row[3:]) for row in data if row[3:]
            )
            if all_stops_missing:
                self.colorValue.emit(3)
                self.stringValue.emit("No measurements in channels:  Stop")
                self.consecutiveErrors = 0
                return cursor_ps, next_bin_edge, photons_in_bin, call_count, total_events, stop_times_ps

            for row in data:
                stops_ps = row[3:]
                if not stops_ps:
                    continue

                # ── Figure (b): accumulate inter-stop deltas on the global timeline ─
                # For each run, prev_t resets to 0 so the first Δt is
                # stop_1 (relative to the virtual start of this run).
                # cursor_ps is advanced by each Δt inside the loop, so it
                # continuously accumulates the real inter-photon intervals and
                # the 10 ms hardware dead time between runs is never included.
                prev_t = 0  # virtual start of this run = t=0
                for t_ps in stops_ps:
                    delta_t = t_ps - prev_t   # Δt between consecutive stops

                    # Skip invalid (negative or zero) deltas
                    if delta_t <= 0:
                        prev_t = t_ps
                        continue

                    # ── KEY FIX ──────────────────────────────────────────────
                    # Advance the continuous timeline cursor by this interval.
                    # Previously abs_t was computed but cursor_ps was NOT
                    # updated here, so every Δt was being added to the same
                    # stale cursor position instead of the running total.
                    cursor_ps += delta_t

                    while cursor_ps >= next_bin_edge:
                        correlator.process_datum(photons_in_bin)
                        photons_in_bin = 0
                        next_bin_edge += self.tau_0

                    photons_in_bin += 1
                    total_events   += 1
                    stop_times_ps.append(delta_t)   # raw stop time for disk save

                    prev_t = t_ps

                # cursor_ps already holds the correct end-of-run position
                # (it accumulated every inter-stop Δt above, which equals
                # stops_ps[-1] relative to this run's virtual start).
                # No extra advance is needed here.

            call_count += 1

            taus, g = correlator.get_correlation_curve()
            if len(taus) > 0:
                self.dataReady.emit(taus, g, np.array(stop_times_ps))

            elapsed = time.time() - t_start
            if self.total_seconds is not None:
                status_str = (
                    f"calls: {call_count} | events: {total_events} | "
                    f"elapsed: {elapsed:.1f} s / {self.total_seconds} s"
                )
            else:
                status_str = (
                    f"calls: {call_count} | events: {total_events} | "
                    f"elapsed: {elapsed:.1f} s"
                )

            if total_events == 0:
                self.colorValue.emit(3)
                self.stringValue.emit("No measurements in channels:  Stop")
            else:
                self.colorValue.emit(1)
                self.stringValue.emit(status_str)
                self.statusUpdate.emit(status_str)

            self.consecutiveErrors = 0

        except Exception as e:
            if isinstance(e, PermissionError) or "PermissionError" in str(e):
                self.consecutiveErrors += 1
            if self.consecutiveErrors > 10:
                self.stop()

        return cursor_ps, next_bin_edge, photons_in_bin, call_count, total_events, stop_times_ps

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