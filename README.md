# Tempico Software 
###
Tempico Software is a suite of tools build to ensure your experience with Tausand's time to digital converter.
###
  - **Language:** Tempico software is written in Python 3.
  - **Functionality:** The software operates via a Graphical User Interface (GUI) which facilitates user interaction with the Tausand Tempico hardware.
  - **Libraries Used:** 
    - PyQT5: Utilizing the API2 provided by pyside2.
    - NumPy
    - PyQtGraph
    - PySerial
    - PyInstaller
    - HID
## UML overview
The UML diagram provides a high-level approximation of the application's structure.
![Uml](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDevBranch/Sources/umlTempico.png)

## Functionality

### Open TempicoSoftware

Tempico software always initializes with a dialog that shows the list of Tempico devices connected to the computer. The user can select one of them to open a connection or cancel and initialize the software without a device. Without a device, the software has only two functionalities: see the About window in the navbar next to Settings or connect a device. If the computer doesn't have a Tempico device connected, the dialog doesn't show any device and you will only be able to cancel or close the window.

![Dialog connect device](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDev/Sources/Dialog.png)


### General settings

The user can configure two parameters of the Tempico device: the first is the threshold voltage and the second is the number of runs. The threshold voltage accepts float numbers between 0.9 V and 1.6 V. The number of runs is a value between 1 and 1000 ( In a single call for measurement, the hardware will execute the specified number of measurements without needing another call for each individual measurement)

![General settings window](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDev/Sources/generalsettings.png)


### Channel settings
The user can configure 5 parameters for each stop channel (A, B, C, D). The first is the average cycles, which are the internal measurements performed before obtaining a single averaged output value. Increasing the cycles improves the precision of the data but also increases the time required for each measurement. The accepted values are 1, 2, 4, 8, 16, 32, 64, and 128. 

The second parameter is the mode. There are 2 modes, and each mode changes the time ranges of data accepted before the start pulse. In mode 1, the accepted values are between 12 ns and 500 ns, and in mode 2, the values are between 125 ns and 4 ms. The two modes are independent of each other (in other words, if you try to measure in mode 2 a value in the range of mode 1, the data will not be registered).

The third parameter is the number of stops. This parameter determines the number of stops that the channel registers after a single start. However, if the channel expects 5 stops and only gets 4, none of the values will be considered in the data. The accepted stops are 1, 2, 3, 4, and 5.

The fourth parameter is the edge type. In each channel, you can decide if the measured data is the beginning of the stop pulse (RISE) or the end of the stop pulse (FALL).

The fifth parameter is the stop mask. It indicates the range of time in which the measurements will be discarded. For example, if the stop mask is 10 µs, the measurements in the range 0 µs - 10 µs will not be taken into account. The stop mask accepts values between 0 µs and 4000 µs.

![Channel settings window](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDev/Sources/settings.png)

### Main window Start-stop histogram
#### Before measurement
Before performing a measurement, the user can configure the channels and the general settings of the device. Using the checkboxes, the user can select which channels they want to appear in the graphics (at least one channel must be selected). After this, the user can press the "Begin Measurement" button. Note: Once a measurement has begun, user will not be able to change the channel settings, general settings, or select an additional channel. In the middle of a measurement, if the user wants to clear the graphic for a specific channel, it is possible to push the "Clear" button for that specific channel. To finish measurement click on the button End measurement. 

![Main window before measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDev/Sources/main.png)

After ending a measurement, if the user desires, they can save the measured data for the Tempico device in txt, csv, or dat format using the "Save" button. If the user wants to adjust the view of the graphic, they can scroll with the mouse to see more detail of the histogram. They can then save the image that appears in the software with the "Save Plots" button. The user can select png, jpg, or tiff as the format for the saved image. The route for the files will be inside of `documents/TempicoSoftwareData`. This folder is created automatically if it doesn't exist when the software is started.


![Main window after measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/JoanDev/Sources/postmeasurement.png)

If the user is not in the middle of a measurement, they will be able to disconnect the Tempico device and connect another if they desire. The data will not be lost if the device is disconnected; data is only lost if the user begins a new measurement.












