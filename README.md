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



