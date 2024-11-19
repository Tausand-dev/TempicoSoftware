# Tempico Software

Tempico Software is a suite of tools built to ensure your experience with Tausand's time-to-digital converter.

The software operates via a Graphical User Interface (GUI) which facilitates user interaction with the Tausand Tempico hardware.

## Libraries Used
- **PyQT5**: Using the API provided by pyside2.
- **NumPy**
- **PyQtGraph**
- **PySerial**
- **PyInstaller**
- **HID**
- **Matplotlib**
- **Scipy**

## UML Overview

The UML diagram provides a high-level approximation of the application’s design structure.

![UML](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/Tempico1.1ClassDiagram.jpeg)

# Functionality

## Open TempicoSoftware  
Tempico software always initializes with a dialog that shows the list of Tempico devices connected to the computer. The user can select one of them to open a connection or cancel and initialize the software without a device. Without a device, the software has only two functionalities: see the About window in the navbar next to Settings or connect a device. If the computer doesn't have a Tempico device connected, the dialog doesn't show any device, and you will only be able to cancel or close the window.

![Connect devices](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/Dialog.png)

## General settings

The user can configure two parameters of the Tempico device: the first is the threshold voltage and the second is the number of runs. The threshold voltage accepts float numbers between 0.9 V and 1.6 V. The number of runs is a value between 1 and 1000 ( In a single call for measurement, the hardware will execute the specified number of measurements without needing another call for each individual measurement)

![General settings](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/generalsettings.png)

## Channel settings
The user can configure 5 parameters for each stop channel (A, B, C, D). The first is the average cycles, which are the internal measurements performed before obtaining a single averaged output value. Increasing the cycles improves the precision of the data but also increases the time required for each measurement. The accepted values are 1, 2, 4, 8, 16, 32, 64, and 128.
The second parameter is the mode. There are 2 modes, and each mode changes the time ranges of data accepted before the start pulse. In mode 1, the accepted values are between 12 ns and 500 ns, and in mode 2, the values are between 125 ns and 4 ms. The two modes are independent of each other (in other words, if you try to measure in mode 2 a value in the range of mode 1, the data will not be registered).
The third parameter is the number of stops. This parameter determines the number of stops that the channel registers after a single start. However, if the channel expects 5 stops and only gets 4, none of the values will be considered in the data. The accepted stops are 1, 2, 3, 4, and 5.
The fourth parameter is the edge type. In each channel, you can decide if the measured data is the beginning of the stop pulse (RISE) or the end of the stop pulse (FALL).
The fifth parameter is the stop mask. It indicates the range of times in which the measurements will be discarded. For example, if the stop mask is 10 µs, the measurements in the range 0 µs - 10 µs will not be considered. The stop mask accepts values between 0 µs and 4000 µs.

![Channel settings](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/settings.png)

## Main window Start-stop histogram

## Before measurement

Before performing a measurement, the user can configure the channels and the general settings of the device. Using the checkboxes, the user can select which channels they want to appear in the graphics (at least one channel must be selected). After this, the user can press the "Begin Measurement" button. Note: Once a measurement has begun, user will not be able to change the channel settings, general settings, or select an additional channel. In the middle of a measurement, if the user wants to clear the graphic for a specific channel, it is possible to push the "Clear" button for that specific channel. To finish measurement click on the button End measurement.

![Before measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/main.png)

## After measurement

After finishing a measurement, if the user desires, they can save the measured data for the Tempico device in txt, csv, or dat format using the "Save" button. If the user wants to adjust the view of the graphic, they can scroll with the mouse to see more detail of the histogram. They can then save the image that appears in the software with the "Save Plots" button. The user can select png, jpg, or tiff as the format for the saved image. The route for the files will be inside documents/TempicoSoftwareData. This folder is created automatically if it doesn't exist when the software is started.

![After measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/postmeasurementStartStop.png)

If the user is not in the middle of a measurement, they will be able to disconnect the Tempico device and connect another if they desire. The data will not be lost if the device is disconnected; data is only lost if the user begins a new measurement.

## FLIM Window
## Before Measurement

Before measurement, the user can define the parameters they want to measure. These include selecting which channel will capture the start pulses and which channel will capture the stop pulses. The user is free to choose any channel; however, if they select a start channel different from the Start Channel, they must connect a signal that emits periodic pulses to capture the differences between the stops. Since the measurements are represented as a frequency histogram, the user can also decide the bin width and the number of bins to plot. These two factors will determine the maximum time range to be graphed. Additionally, the user can choose how many measurements to perform. It is important to note that the mode change has no effect, as the mode will adjust automatically according to the maximum time range.

![Before measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/PreMeasurement.png)

## During Measurement

While the measurement is in progress, the user can monitor several parameters. The first is the total number of successful measurements, meaning those in which both a start and a stop were captured within the specified time range. Another parameter is the total number of start pulses, which indicates how many start pulses have been received, regardless of whether a stop was captured. The total measurement time is also displayed, measured by a timer that starts when the measurement begins. The user has a status bar that indicates the percentage of the measurement completed or whether any channel is not receiving pulses.

![During measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/MientrasMedicion.png)

## After Measurement

After the measurement, the user can decide whether to save the image of the data or the raw data, which are saved by default in the Documents/TempicoSoftwareData directory. Additionally, the user can adjust the graph by specifying the fitting parameters. Four types of fitting are available: Exponential, Kohlrausch, Shifted Exponential, and Double Exponential. The fitting parameters are determined along with an R² value to assess the quality of the fit. If a fit was performed, the values are saved both in the graph's footer and alongside the raw data.

![After measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/Postmeasurement.png)

![Fit measurement](https://github.com/Tausand-dev/TempicoSoftware/blob/FLIMtest/Sources/AfterFit.png)

## For Developers

To test the system, first clone the repository and then set the console path to the `src` folder. Once there, run the following command: `pip install -r requirements.txt`. From the console, in the same path, run `python main.py`. This will allow the program to run correctly (if using a Linux-based OS, use `sudo` at the beginning). If the command does not work, use `python3 main.py`. 

**Note**: It is recommended to use Python version 3.8.10 (32-bit).

To generate the executable, run the following command: `pyinstaller --additional-hooks-dir installers/pyinstaller_hooks/ --name TempicoSoftware --onefile --noconsole -i Sources/tausand_small.ico main.py`. This will generate a single file containing the program. To run it correctly, this file must be placed inside the `Sources` folder that contains the images.

## Step 1: Download and Install Inno Setup Compiler
First, download the Inno Setup Compiler program and install it on your machine. The download page for the program is available at the following link: [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php). Download the `.exe` file corresponding to the application installer.

## Step 2: Open Inno Setup Compiler
Once Inno Setup is installed correctly, open it and follow these steps:

1. First, you will be prompted to either open an existing script or create a new one. Select the option to **Create a New Script Using the Wizard**.

![Step 1](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial1.png)

2. In the next window, leave all options unselected and click **Next**.

![Step 2](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial2.png)

3. You will then be asked to provide the application name, version, publisher, and website (if applicable). For Tempico Software, use the following values for each field.

![Step 3](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial3.png)

4. Next, specify the default folder for the application and the application name. If these values do not carry over from the previous step, use the specified values provided.

![Step 4](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial4.png)

5. In the field **Application Main Executable File**, provide the path to the executable created earlier with PyInstaller. Additionally, click on **Add Folder** to include the images needed by the executable. Locate and select the `Sources` folder containing these image files. Leave all other fields as their default values.

![Step 5](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial5.png)

6. For the next four windows, leave the default values as they are (ensure they match the values shown in the provided screenshots).

![Step 6](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial6.png)

![Step 6](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial7.png)

![Step 6](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial8.png)

![Step 6](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial9.png)

7. You will be prompted to select the installation language. Since Tempico Software only supports English for this version, select **English**.

![Step 7](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial10.png)

8. In the **Custom Compiler Output Folder** field, specify the directory where the installer will be saved once compiled. This path is flexible and should be chosen based on the developer’s preference. In the **Compiler Output Base File Name** field, enter `Tempico Software Setup`. For **Custom Setup Icon File**, locate the `Sources` folder and select the `tausand_small.ico` icon file. Leave the password field empty.

![Step 8](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial11.png)

9. For the following windows, simply click **Next** and then **Finish**, keeping the default values unchanged.

![Step 9](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial12.png)

![Step 9](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial13.png)
10. Once the setup wizard is completed, a window will appear asking if you want to compile the file. Click **Yes**. Another window will ask if you want to save the script. Click **Yes** and select the path to your GitHub project, saving it in the `installer` folder and naming the file appropriately. Wait for the file to compile; this will automatically generate the installer in the specified output folder, from which you can run the installer.


![Step 10](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial14.png)

![Step 10](https://github.com/Tausand-dev/TempicoSoftware/blob/main/ReadmeSources/Tutorial15.png)

