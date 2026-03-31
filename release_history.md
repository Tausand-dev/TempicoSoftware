# Release Notes 2.0.0 – January 2026

## New Features

- Added compatibility with **TP12XX** devices, enabling the measurement of negative time intervals of down to -200 ns relative to the start signal.
- Introduced an internal periodic pulse generator, allowing configurable signal generation directly within the Tempico device for both start and stop channels.

---

# Release Notes 1.3.0 – November 2025

## New Features

- Introduced the **Time Stamping** tab, a high-performance acquisition mode designed to capture pulse arrival times from start and stop channels with maximum throughput. This feature is optimized to minimize data loss, ensuring reliable acquisition even at high event rates. It enables the storage of large volumes of timestamp data for further analysis, supporting precise temporal characterization of signals.

---

# Release Notes 1.2.1 – July 2025

## Bug Fixes

- Fixed bugs in the **Counts Estimated** tab that caused incorrect readings or inconsistent updates.
- Added **visualization options** for estimated count graphs, allowing users to switch between **Free Navigation** and **Full Range** display modes for better control.

---

# Release Notes 1.2.0 – July 2025

## New Features

- Introduced the **Counts Estimation** tab, which displays **per-second estimations** of counts received by each channel.
- View of the **historical count estimations** as well as **current counts**.
- Both the generated data and their corresponding graphs can be **saved for later analysis**.

---

# Release Notes 1.1.0 – March 2025

## New Features

- Added support for **Lifetime Measurements**, generating graphs based on detected frequency events.
- Support for different types of **exponential fitting** on captured data:
  - **Kohlrausch exponential fits**
  - **Shifted exponentials** (with one parameter offset)
  - **Double exponentials**
- Users can:
  - Define the **number of measurements** to perform per start event.
  - Choose the **time range** to be measured.
  - Set the **bin size** for histogram grouping.
- Included **status bars** to display the current state of the measurement in real time.

---

# Release Notes 1.0.0 – November 2024

## New Features

- Introduced **Start-Stop Histogram measurements**, which record time intervals between start events and those detected by the stop channel.
- Data is organized into a **histogram view**.
- Users can choose to:
  - Save only the **raw data**, or
  - Also **save the generated histogram image**.

