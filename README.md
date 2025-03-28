# Tempico Software

Tempico Software is a suite of tools built to ensure your experience with Tausand's time-to-digital converter.

The software operates via a Graphical User Interface (GUI) which facilitates user interaction with the Tausand Tempico hardware.

## Libraries Used

- **HID**
- **Matplotlib**
- **NumPy**
- **PyInstaller**
- **PyQT5**: Using the API provided by pyside2.
- **PyQtGraph**
- **PySerial**
- **PyTempico**
- **Scipy**

## UML Overview

The UML diagram provides a high-level approximation of the application’s design structure.

![UML](./Sources/Tempico1.1ClassDiagram.jpeg)

# Functionality

## Open TempicoSoftware

Tempico software always initializes with a dialog that shows the list of Tempico devices connected to the computer. The user can select one of them to open a connection or cancel and initialize the software without a device. Without a device, the software has only two functionalities: see the About window in the navbar next to Settings or connect a device. If the computer doesn't have a Tempico device connected, the dialog doesn't show any device, and you will only be able to cancel or close the window.

![Connect devices](./Sources/Dialog.png)

## General settings

The user can configure two parameters of the Tempico device: the first is the threshold voltage and the second is the number of runs. The threshold voltage accepts float numbers between 0.9 V and 1.6 V. The number of runs is a value between 1 and 1000 ( In a single call for measurement, the hardware will execute the specified number of measurements without needing another call for each individual measurement)

![General settings](./Sources/generalsettings.png)

## Channel settings

The user can configure 5 parameters for each stop channel (A, B, C, D). The first is the average cycles, which are the internal measurements performed before obtaining a single averaged output value. Increasing the cycles improves the precision of the data but also increases the time required for each measurement. The accepted values are 1, 2, 4, 8, 16, 32, 64, and 128.

The second parameter is the mode. There are 2 modes, and each mode changes the time ranges of data accepted before the start pulse. In mode 1, the accepted values are between 12 ns and 500 ns, and in mode 2, the values are between 125 ns and 4 ms. The two modes are independent of each other (in other words, if you try to measure in mode 2 a value in the range of mode 1, the data will not be registered).

The third parameter is the number of stops. This parameter determines the number of stops that the channel registers after a single start. However, if the channel expects 5 stops and only gets 4, none of the values will be considered in the data. The accepted stops are 1, 2, 3, 4, and 5.

The fourth parameter is the edge type. In each channel, you can decide if the measured data is the beginning of the stop pulse (RISE) or the end of the stop pulse (FALL).

The fifth parameter is the stop mask. It indicates the range of times in which the measurements will be discarded. For example, if the stop mask is 10 µs, the measurements in the range 0 µs - 10 µs will not be considered. The stop mask accepts values between 0 µs and 4000 µs.

![Channel settings](./Sources/settings.png)

## Main window Start-stop histogram

### Before measurement

Before performing a measurement, the user can configure the channels and the general settings of the device. Using the checkboxes, the user can select which channels they want to appear in the graphics (at least one channel must be selected). After this, the user can press the "Begin Measurement" button. Note: Once a measurement has begun, user will not be able to change the channel settings, general settings, or select an additional channel. In the middle of a measurement, if the user wants to clear the graphic for a specific channel, it is possible to push the "Clear" button for that specific channel. To finish measurement click on the button End measurement.

![Before measurement](./Sources/main.png)

### After measurement

After finishing a measurement, if the user desires, they can save the measured data for the Tempico device in txt, csv, or dat format using the "Save" button. If the user wants to adjust the view of the graphic, they can scroll with the mouse to see more detail of the histogram. They can then save the image that appears in the software with the "Save Plots" button. The user can select png, jpg, or tiff as the format for the saved image. The route for the files will be inside documents/TempicoSoftwareData. This folder is created automatically if it doesn't exist when the software is started.

![After measurement](./Sources/postmeasurementStartStop.png)

If the user is not in the middle of a measurement, they will be able to disconnect the Tempico device and connect another if they desire. The data will not be lost if the device is disconnected; data is only lost if the user begins a new measurement.

## FLIM Window

### Before Measurement

Before measurement, the user can define the parameters they want to measure. These include selecting which channel will capture the start pulses and which channel will capture the stop pulses. The user is free to choose any channel; however, if they select a start channel different from the Start Channel, they must connect a signal that emits periodic pulses to capture the differences between the stops. Since the measurements are represented as a frequency histogram, the user can also decide the bin width and the number of bins to plot. These two factors will determine the maximum time range to be graphed. Additionally, the user can choose how many measurements to perform. It is important to note that the mode change has no effect, as the mode will adjust automatically according to the maximum time range.

![Before measurement](./Sources/PreMeasurement.png)

### During Measurement

While the measurement is in progress, the user can monitor several parameters. The first is the total number of successful measurements, meaning those in which both a start and a stop were captured within the specified time range. Another parameter is the total number of start pulses, which indicates how many start pulses have been received, regardless of whether a stop was captured. The total measurement time is also displayed, measured by a timer that starts when the measurement begins. The user has a status bar that indicates the percentage of the measurement completed or whether any channel is not receiving pulses.

![During measurement](./Sources/MientrasMedicion.png)

### After Measurement

After the measurement, the user can decide whether to save the image of the data or the raw data, which are saved by default in the Documents/TempicoSoftwareData directory. Additionally, the user can adjust the graph by specifying the fitting parameters. Four types of fitting are available: Exponential, Kohlrausch, Shifted Exponential, and Double Exponential. The fitting parameters are determined along with an R² value to assess the quality of the fit. If a fit was performed, the values are saved both in the graph's footer and alongside the raw data.

![After measurement](./Sources/Postmeasurement.png)

![Fit measurement](./Sources/AfterFit.png)

## Grant port access on Linux

Most Linux configurations have a dialout group for full and direct access to serial ports. By adding your user account to this group you will have the necessary permissions for Tempico Software to communicate with the serial ports.

1. Open Terminal.

2. Enter the following command, replacing ```<username>``` with the name of your account.

```
sudo usermod -a -G dialout <username>   
```

3. Sign in and out for the changes to take effect.

## For Developers

### Updating to a new version

Modify the version number in the following files:

* installer/installer_builder.iss

* TempicoSoftware/constants.py

### Creating a virtual environment

Run the following code to create a virtual environment called `.venv`

```
python -m venv .venv
```

#### Activate

- On Unix systems:
  
  ```
  source .venv/bin/activate
  ```

- On Windows:
  
  ```
  .venv\Scripts\activate
  ```

#### Deactivate

```
deactivate
```

### Installing packages

After the virtual environment has been activated, install required packages by using:

```
python -m pip install -r requirements.txt
```

From the console, in the same path of the cloned project, run 

```
python src/main.py
```

This will allow the program to run correctly (if using a Linux-based OS, use `sudo` at the beginning). If the command does not work, use `python3 main.py`. 

**Note**: It is recommended to use Python version 3.8.10 (32-bit).

To generate the executable, run the following command:

```
pyinstaller --additional-hooks-dir installers/pyinstaller_hooks/ --name TempicoSoftware --onefile --noconsole -i Sources/tausand_small.ico src/main.py
```

Two folders will be created: build and dist. Inside `dist` you'll find the `.exe` file. To run it correctly, this file must be placed next to the `Sources` folder that contains the images.

### Generate Installer

Once the executable is compiled, we will proceed to create the software installer.

#### Step 1: Download and Install Inno Setup Compiler

First, download the Inno Setup Compiler program and install it on your machine. The download page for the program is available at the following link: [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php). Download the `.exe` file corresponding to the application installer.

#### Step 2a: Create using iss file at Inno Setup Compiler

Using the File Explorer, go to the folder `installer` and double-click `installer_builder.iss` or open it from Inno Setup if it is already opened. Click on the play icon and then follow the process, which includes the creation of the installer and the installation itself.

The installer will be saved in a folder called `Output`.

If the `.iss` file does not exist, follow step 2b.

#### Step 2b: Create using Inno Setup Compiler Wizard

Once Inno Setup is installed correctly, open it and follow these steps:

1. First, you will be prompted to either open an existing script or create a new one. Select the option to **Create a New Script Using the Wizard**.

![Step 1](./ReadmeSources/Tutorial1.png)

2. In the next window, leave all options unselected and click **Next**.

![Step 2](./ReadmeSources/Tutorial2.png)

3. You will then be asked to provide the application name, version, publisher, and website (if applicable). For Tempico Software, use the following values for each field.

![Step 3](./ReadmeSources/Tutorial3.png)

4. Next, specify the default folder for the application and the application name. If these values do not carry over from the previous step, use the specified values provided.

![Step 4](./ReadmeSources/Tutorial4.png)

5. In the field **Application Main Executable File**, provide the path to the executable created earlier with PyInstaller. Additionally, click on **Add Folder** to include the images needed by the executable. Locate and select the `Sources` folder containing these image files. Leave all other fields as their default values.

![Step 5](./ReadmeSources/Tutorial5.png)

6. For the next four windows, leave the default values as they are (ensure they match the values shown in the provided screenshots).

![Step 6](./ReadmeSources/Tutorial6.png)

![Step 6](./ReadmeSources/Tutorial7.png)

![Step 6](./ReadmeSources/Tutorial8.png)

![Step 6](./ReadmeSources/Tutorial9.png)

7. You will be prompted to select the installation language. Since Tempico Software only supports English for this version, select **English**.

![Step 7](./ReadmeSources/Tutorial10.png)

8. In the **Custom Compiler Output Folder** field, specify the directory where the installer will be saved once compiled. This path is flexible and should be chosen based on the developer’s preference. In the **Compiler Output Base File Name** field, enter `Tempico Software Setup`. For **Custom Setup Icon File**, locate the `Sources` folder and select the `tausand_small.ico` icon file. Leave the password field empty.

![Step 8](./ReadmeSources/Tutorial11.png)

9. For the following windows, simply click **Next** and then **Finish**, keeping the default values unchanged.

![Step 9](./ReadmeSources/Tutorial12.png)

![Step 9](./ReadmeSources/Tutorial13.png)
10. Once the setup wizard is completed, a window will appear asking if you want to compile the file. Click **Yes**. Another window will ask if you want to save the script. Click **Yes** and select the path to your GitHub project, saving it in the `installer` folder and naming the file appropriately. Wait for the file to compile; this will automatically generate the installer in the specified output folder, from which you can run the installer.

![Step 10](./ReadmeSources/Tutorial14.png)

![Step 10](./ReadmeSources/Tutorial15.png)

#### MacOS

Run the following command

```
pyinstaller --additional-hooks-dir installers/pyinstaller_hooks/ --name TempicoSoftware --onefile --noconsole -i Sources/tausand_small.png src/main.py
```

Two folders will be created: build and dist. Inside `dist` you'll find the `.app` file. This file can be run from a console by executing the command.
To change the icon of the `.app` file follow the instructions here https://appleinsider.com/articles/21/01/06/how-to-change-app-icons-on-macos

#### Linux

Run the following command

```
pyinstaller --additional-hooks-dir installers/pyinstaller_hooks/ --name TempicoSoftware --onefile --noconsole -i Sources/tausand_small.png src/main.py
```

Two folders will be created: build and dist. Inside dist you'll find the executable file. This file can be run from a console by executing the command

```
./TempicoSoftware
```

If it doesn't run, make sure it has execute permissions. In case it doesn't run `chmod +x TempicoSoftware` and then try again. The executable file could be used to create a Desktop entry so it can be lauched as an application (for example in Gnome, an icon could be assigned)

To create an AppImage that can be run from multiple Linux distributions and be launch by double clicking, follow the next steps.

* Create the following folder path: 
    TempicoSoftware.AppDir/usr/bin
* Place the executable inside the bin folder 
* Place the Sources folder inside the bin folder
* Place the icon tausand_small.png located at Sources/tausand_small.png inside TempicoSoftware.AppDir
* Create a file called TempicoSoftware.desktop inside TempicoSoftware.AppDir
* Edit the `.desktop` file with the following

```
[Desktop Entry]
Name=TempicoSoftware
Exec=TempicoSoftware
Icon=tausand_small
Type=Application
Categories=Utility;
```

* Give execution permisions to the `.desktop` file: `chmod +x TempicoSoftware.desktop`
* Create a script called `AppRun` with the following contents

```
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
EXEC="${HERE}/usr/bin/TempicoSoftware"
exec "${EXEC}"
```

* Give execution permisions to the `AppRun` file: `chmod +x AppRun`. After this step, the app should run after doing `./AppRun` on a Terminal.

* For 64-bit architecture, download appimagetool-x86_64.AppImage from https://github.com/AppImage/AppImageKit/releases/ and give execution permisions to it. 

* Place appimagetool outside TempicoSoftware.AppDir and run

```
  ARCH=x86_64 ./appimagetool-x86_64.AppImage TempicoSoftware.AppDir
```

* The file `TempicoSoftware-x86_64.AppImage` will be created. This file can be opened by double clicking it.

## Generate sphinx documentation

### First time generating

The first thing we need to do is verify that the Sphinx library is installed in our environment. If it is not installed, we can do so with the command:

```
pip install sphinx
```

If it doesn't work, we use:

```
pip3 install sphinx
```

Next, we need to install the theme used for the documentation; to do this, run the command:

```
pip install sphinx-rtd-theme
```

Next, within the repository folder where the project is located, we will create a new folder called `docs`. To create the base folder for our project, run the `sphinx-quickstart` command on the `docs` folder. The project will be named "Tempico Software", and the version will correspond to the one on which the software documentation is being created. We will leave the language set to English.

Inside the `docs` folder, several files will have been generated, one of which is called `conf.py`. This file contains a list called `extensions`; within it, we will add the following extensions:

```
"sphinx.ext.todo", "sphinx.ext.autodoc", "sphinx.ext.viewcode"
```

We will also change the script's path so that when it runs, it can recognize the scripts inside the `src` folder. To do this, we add the following line of code at the beginning, even before the imports:

```
sys.path.insert(0, os.path.abspath('../src'))  
```

Now there should be a text variable called `html_theme`; here, we will change the default theme and set it to `sphinx_rtd_theme`.

After that, we must execute the following command:

```
sphinx-apidoc -o docs ./src
```

This will create a `.rst` file in the `docs` folder for each of the Python scripts we have for the application. Many of these scripts contain information about graphical interfaces or may even be auxiliary; it is not necessary to document them, so we can delete their `.rst` files. Only the names of the files that have not been deleted should remain in the `modules.rst` file.

Inside `docs`, we will create a folder called `sources` and place the Tempico Software logo there. Then, we will edit the file called `index.rst` and place the logo at the beginning as follows:

```
.. figure:: sources/image.png
   :scale: 60 %
   :alt: Tausand logo
   :align: center
```

Under the title, we will add the description of the software, outlining each of the functionalities.

Next, we need to configure the `index.rst` file. By default, the following block is created:

```
.. toctree:: :maxdepth: 1 :caption: Contents:
```

Below this block, leaving a blank line, we need to add all the modules with `.rst` at the end of each one.

Finally, what we will do is change the value of `_build` to `build` in the `exclude_patterns` variable in the `conf.py` file. We will also make this change in the `make.bat` file on the line `set BUILDDIR`, and in the `Makefile` under the `BUILDDIR` setting.

Once we are sure that all the modules to be documented have a `.rst` file and are included in the `modules.rst` file, we will generate the documentation by running the following command in the `docs` folder:

```
.\make.bat html
```

The generated HTML file will be found inside the `build` folder.

To generate a PDF file, we first need to download and install MikTeX and Strawberry Perl. This can be done from the following websites: [https://miktex.org/download](https://miktex.org/download) and [https://strawberryperl.com](https://strawberryperl.com). Afterward, we need to add both programs to the environment variables. Once this process is complete, we can verify that everything is working correctly by executing the following command:

```
latexmk --version
```

Then, inside the `docs` folder, we execute the following command:

```
.\make.bat latexpdf
```

This will generate our documentation in PDF format.

### Generate documentation for a new version

If we create a new script for a new version that has not been documented yet is not necessary to run all steps executed before. However we need to run the following command again:

```
sphinx-apidoc -o docs ./src
```

This will regenerate all `.rst` files for all Python scripts inside the `.src` folder. We must again remove the `.rst` files for the modules that were not documented and delete them from `modules.rst`. It is necessary to reconfigure the `index.rst` file as specified in previous steps.

Make sure that in the `make.bat` file, the `BUILDDIR` variable is set to `build` and not `_build`, and do the same in the `Makefile`. If that's the case, simply change them.

After this , we can run the commands again to generate the documentation according to the required format:

```
.\make.bat html
```

```
.\make.bat latexpdf
```

If the developer did not create a new script, they only need to run the previous commands to update the documentation.


