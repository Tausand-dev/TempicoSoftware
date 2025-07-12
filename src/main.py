from PySide2.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMessageBox, QSplashScreen, QApplication, QMainWindow, QAction
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import QTimer, QSize, Qt
from PySide2.QtWidgets import QWidget, QTabWidget, QSystemTrayIcon
from generalsettings import GeneralSettingsWindow
from aboutDialog import Ui_AboutDialog
from ui_StarStopHistogram import Ui_HistogramaStartStop
from ui_g2measurement import Ui_G2
from ui_devicesDialog import Ui_Devices
import time
from PySide2.QtCore import QTimer
import time
from ui_CountsEstimated import Ui_CountsEstimated
from ui_TimeStamping import Ui_TimeStamping
#To do eliminate import
from createsavefile import createsavefile as savefile
from ui_settings import Ui_settings
from uiParametersDialog import UiParameters
from ParametersDialog import CountParameters
from StartStopHist import StartStopLogic
from constants import *
from ui_LifeTimemeasurement import UiLifeTime
from LifeTimeGraphics import LifeTimeGraphic
from CountsEstimatedGraphics import CountEstimatedLogic
from timeStampGraphics import TimeStampLogic
import sys
import math
#from qt_material import apply_stylesheet



class SplashScreen(QMainWindow):
    """
    Splash screen class for the application.

    This class creates a splash screen that displays an image for a brief period before fading out and transitioning to the main application window.

    The key responsibilities of this class include:
    - Displaying a splash screen with a specified image.
    - Timing the display duration and handling the transition to the main application window.

    :param parent: The parent widget (optional).
    :type parent: QWidget, optional
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Splash Screen")
        self.setFixedSize(400, 300)


        # Crear una etiqueta para mostrar la imagen
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 400, 300)

        # Cargar la imagen
        pixmap = QPixmap(BANNER)  # Ajusta la ruta de tu imagen
        self.image_label.setPixmap(pixmap)

        # Mostrar la ventana principal después de 3 segundos
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_main_window)
        self.timer.start(1000)  # Tiempo en milisegundos

    def show_main_window(self):
        """
        Displays the main window of the application.

        This function creates an instance of the main window (`MainWindow`) and displays it.
        After showing the main window, it closes the current window.

        It does not take any parameters and does not return a value.
        :returns: None
        """
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    """
    Main application window class.

    This class is responsible for creating the main window of the application, including its tabs and graphical user interface (GUI) components.
    It serves as a bridge between the UI classes that handle the design elements and the logic classes that manage the application's functionalities.

    The main tasks of this class include:
    - Initializing the main window and its layout.
    - Creating and managing tabs for different sections of the application.
    - Integrating UI design elements with the logical operations for each functionality.

    :param parent: The parent widget (optional).
    :param args: Additional arguments.
    :type parent: QWidget, optional
    :type args: tuple
    """
    def __init__(self, parent=None, *args):
        super(MainWindow,self).__init__(parent=parent)
        #------Window parameters---------#
        self.savefile=savefile()
        self.savefile.create_folder_and_file()
        self.setWindowTitle("Tempico Software")
        self.setGeometry(100,100,1000,700)
        self.setWindowIcon(QIcon(ICON_LOCATION))
        self.setMinimumSize(1100,800)
        self.conectedDevice=None
        self.LifeTimeTimer=QTimer()
        self.LifeTimeTimer.timeout.connect(self.manageConection)
        self.currentMeasurement=False
        # save old settings state
        self.averageCycleChannelA= 0
        self.averageCycleChannelB= 0
        self.averageCycleChannelC= 0
        self.averageCycleChannelD= 0
        #
        self.modeChangeChannelA= 0
        self.modeChangeChannelB= 0
        self.modeChangeChannelC= 0
        self.modeChangeChannelD= 0
        #
        self.numberOfStopsChannelA=0
        self.numberOfStopsChannelB=0
        self.numberOfStopsChannelC=0
        self.numberOfStopsChannelD=0
        #
        self.edgeTypeChannelA=0
        self.edgeTypeChannelB=0
        self.edgeTypeChannelC=0
        self.edgeTypeChannelD=0
        #
        self.stopMaskChannelA=0
        self.stopMaskChannelB=0
        self.stopMaskChannelC=0
        self.stopMaskChannelD=0
        ##
        self.openSettings=False
        self.openGeneralSettings=False
        ## general settings
        self.thresholdVoltage=0
        self.numberRuns=0

        if sys.platform == 'win32':
            import ctypes
            myappid = APPID  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        elif sys.platform == 'linux':
            tray_icon = QSystemTrayIcon(QIcon(ICON_LOCATION), self)
            tray_icon.setToolTip("Tempico Software")



        #------Menu bar-------------#
        menu_bar = self.menuBar()
        #file_menu = menu_bar.addMenu("File")
        settings_menu = menu_bar.addMenu("Settings")
        #help_menu = menu_bar.addMenu("Help")
        about_menu = menu_bar.addMenu("About")
        #Parameters_menu



        #parameters_menu=menu_bar.addMenu("Parameters")


        #-----Actions for file--------#
        #save_action=QAction("Save",self)
        #new_action=QAction("New",self)
        #Open_action=QAction("Open",self)
        #file_menu.addAction(save_action)
        #file_menu.addAction(new_action)
        #file_menu.addAction(Open_action)
        #-----Actions for settings--------#
        change_parameters_action=QAction("Channels settings",self)
        settings_menu.addAction(change_parameters_action)
        change_parameters_action.triggered.connect(self.settings_clicked)
        general_settings_action=QAction("General settings",self)
        settings_menu.addAction(general_settings_action)
        general_settings_action.triggered.connect(self.general_settings_clicked)
        about_settings_action=QAction("About Tempico Software",self)
        about_settings_action.triggered.connect(self.about_settings)
        about_menu.addAction(about_settings_action)
        #parameters_settings_action=QAction("Get Count Parameters",self)
        #parameters_settings_action.triggered.connect(self.parameters_action)
        #parameters_menu.addAction(parameters_settings_action)

        #-----Qtabs for every type of measure--------#
        self.tabs=QTabWidget(self)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tab4=QWidget()
        self.tabs.addTab(self.tab1,"Start-Stop histogram")
        self.tabs.addTab(self.tab2,"Lifetime")
        self.tabs.addTab(self.tab3,"Counts Estimation")
        self.tabs.addTab(self.tab4,"TimeStamping")
        #self.tabs.addTab(self.tab3,"g2 Measurement")
        self.tabs.setGeometry(0,20,1000,700)
        # Crear un QVBoxLayout para agregar el QTabWidget
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        #layout.setContentsMargins(0, 30, 0, 0)
        # Establecer el layout en la ventana principal
        self.sentinel1=0
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.construct_start_stop_histogram(self.tab1)
        self.connectButton = QPushButton("Connect", self)
        self.disconnectButton = QPushButton("Disconnect", self)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.connectButton)
        buttonLayout.addWidget(self.disconnectButton)

        # Crear un QWidget para contener los QTabWidget y los botones
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        #------g2 Graphic class---------#
        self.g2Graphic=None
        self.LifeTimeGraphic=None
        self.g2_init_sentinel=0
        self.initg2DialogSentinel=0
        #------LifeTime Graphic class---------#
        self.LifeTimeGraphic=None
        self.LifeTime_init_sentinel=0
        #------Counts Estimated Graphic class---------#
        self.countsEstimatedGraphic=None
        self.countsEstimated_init_sentinel=0
        #------Time Stamping Graphic class---------#
        self.timeStampGraphic=None
        self.timeStampGraphic_init_sentinel=0
        

        #------Layout for the main window---------#
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.addWidget(self.tabs)
        self.connectsentinel=0
        self.connectButton.clicked.connect(self.open_dialog)
        self.disconnectButton.clicked.connect(self.disconnect_button_click)
        self.sentinel2=0
        self.sentinel3=0
        self.sentinel4=0
        self.tabs.currentChanged.connect(self.clicked_tabs)
        self.show()
        self.open_dialog()
        self.show()


    #-----Functions for construc every Qtab--------#
    def construct_start_stop_histogram(self,parent):
        """
        Constructs the Start/Stop Histogram window.

        This function takes a `QTabWidget` parent, and if the sentinel is not set, it creates
        an instance of the `Ui_HistogramaStartStop` class and sets up the UI using the given parent.

        It does not return a value.

        :param parent: The parent widget (typically a `QTabWidget`) for the histogram window.
        :type parent: QWidget
        :returns: None
        """
        if self.sentinel1==0:
            self.ui = Ui_HistogramaStartStop()
            self.ui.setupUi(parent)
            self.sentinel1=1

    def construct_lifetime(self,parent):
        """
        Constructs the Lifetime Measurements window.

        This function takes a `QTabWidget` parent, and if the sentinel is not set, it creates
        an instance of the `UiLifeTime` class and sets up the UI using the given parent.

        It does not return a value.

        :param parent: The parent widget (typically a `QTabWidget`) for the lifetime measurements window.
        :type parent: QWidget
        :returns: None
        """
        if self.sentinel2==0:
            self.uiLifeTime = UiLifeTime()
            self.uiLifeTime.setupUi(parent)
            self.sentinel2=1

    def construct_counts_estimated(self,parent):
        """
        Constructs the Counts Estimated window.

        This function takes a `QTabWidget` parent, and if the sentinel is not set,
        it creates an instance of the `Ui_CountsEstimated` class and sets up the UI using the given parent.

        It ensures the UI is initialized only once by checking the `sentinel3` flag.

        :param parent: The parent widget (typically a `QTabWidget`) for the counts estimated window.
        :type parent: QWidget
        :returns: None
        """
        #TO DO Build Documentation
        if self.sentinel3==0:
            self.uiCountsEstimated = Ui_CountsEstimated()
            self.uiCountsEstimated.setupUi(parent)
            self.sentinel3=1
    
    
    def construct_time_stamping(self,parent):
        """
        Constructs the Counts Estimated window.

        This function takes a `QTabWidget` parent, and if the sentinel is not set,
        it creates an instance of the `Ui_CountsEstimated` class and sets up the UI using the given parent.

        It ensures the UI is initialized only once by checking the `sentinel3` flag.

        :param parent: The parent widget (typically a `QTabWidget`) for the counts estimated window.
        :type parent: QWidget
        :returns: None
        """
        #TO DO Build Documentation
        if self.sentinel4==0:
            self.uiTimeStamping = Ui_TimeStamping()
            self.uiTimeStamping.setupUi(parent)
            self.sentinel4=1



    def construct_g2(self,parent):
        """
        Constructs the g2 Measurements window.

        This function takes a `QTabWidget` parent, and if the sentinel is not set, it creates
        an instance of the `Uig2` class and sets up the UI using the given parent.

        It does not return a value.

        :param parent: The parent widget (typically a `QTabWidget`) for the lifetime measurements window.
        :type parent: QWidget
        :returns: None
        """
        if self.sentinel3==0:
            self.uig2 = Ui_G2()
            self.uig2.setupUi(parent)
            self.sentinel3=1

    def open_dialog(self):
        """
        Opens a dialog window to detect and connect a measurement device.

        This function creates and displays a dialog window that lists available measurement devices and their corresponding ports.
        Users can select a device and either connect or cancel the operation.

        If the 'Connect' button is clicked:
        - The selected device is connected, and all relevant software options are enabled.
        - The function tries to open the device and, upon success, interacts with graphical components (if any are present) to reflect the connected status.

        If the 'Cancel' button is clicked:
        - No options are activated.

        In case of a connection error, a message box is displayed informing the user of the failure.

        :returns: None
        """
        self.dialog=QDialog(self)
        self.uidialog = Ui_Devices()
        self.uidialog.setupUi(self.dialog)
        self.dialog.exec_()
        self.conectedDevice=  self.uidialog.deviceConnected
        if self.conectedDevice!=None:
            if self.connectsentinel==0:
                self.connectButton.setEnabled(False)
                self.disconnectButton.setEnabled(True)
                try:
                    self.conectedDevice.open()
                    self.LifeTimeTimer.start(500)
                    if self.g2Graphic!=None:
                         self.g2Graphic.connectDevice()
                    if self.LifeTimeGraphic!=None:
                        self.LifeTimeGraphic.connectedDevice(self.conectedDevice)
                    if self.countsEstimatedGraphic!=None:
                        self.countsEstimatedGraphic.connectedDevice(self.conectedDevice)
                    #To do implement connect device
                    if self.timeStampGraphic!=None:
                        self.timeStampGraphic.connectedDevice(self.conectedDevice)


                    checkchannel1=self.ui.Channel1Graph1
                    checkchannel2=self.ui.Channel4Graph1
                    checkchannel3=self.ui.Channel2Graph1
                    checkchannel4=self.ui.Channel3Graph1
                    startbutton=self.ui.SaveGraph1
                    stopbutton=self.ui.StopGraph1
                    savebutton=self.ui.SaveDoc
                    #Save Plots
                    save_graph_1=self.ui.SaveImage1

                    #Clear Plots
                    clear_channel_A=self.ui.ClearchannelA
                    clear_channel_B=self.ui.ClearchannelB
                    clear_channel_C=self.ui.ClearchannelC
                    clear_channel_D=self.ui.ClearchannelD

                    channel1=self.conectedDevice.ch1

                    channel2=self.conectedDevice.ch2

                    channel3=self.conectedDevice.ch3

                    channel4=self.conectedDevice.ch4


                    self.connectsentinel=1
                    self.grafico=StartStopLogic(self.ui.Graph3,self.disconnectButton,self.conectedDevice,checkchannel1,checkchannel2,checkchannel3,checkchannel4,startbutton,stopbutton,savebutton,save_graph_1,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D, self.connectButton,self, self.ui.valueStatusLabel,self.ui.pointLabel, self.LifeTimeTimer)

                except:
                    self.LifeTimeTimer.stop()
                    msg_box = QMessageBox(self)
                    msg_box.setText("Connection with the device failed. Check if another software is using the Tempico device or verify the hardware status.")
                    msg_box.setWindowTitle("Connection Error")
                    pixmap= QPixmap("/Sources/tausand_small.ico")
                    msg_box.setIconPixmap(pixmap)
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
                    self.connectButton.setEnabled(True)
                    self.disconnectButton.setEnabled(False)

            else:
                if hasattr(self, 'grafico'):  # Verificar si self.grafico está definido
                    try:
                        openSentinel=False
                        try:
                            self.conectedDevice.open()
                            self.LifeTimeTimer.start(500)
                            openSentinel=True
                        except:
                            self.LifeTimeTimer.stop()
                        if self.g2Graphic!=None and openSentinel:
                             self.g2Graphic.connectDevice()
                        if self.LifeTimeGraphic!=None and openSentinel:
                            self.LifeTimeGraphic.connectedDevice(self.conectedDevice)
                        if self.countsEstimatedGraphic!=None and openSentinel:
                            self.countsEstimatedGraphic.connectedDevice(self.conectedDevice)
                        if self.timeStampGraphic!=None and openSentinel:
                            self.timeStampGraphic.connectedDevice(self.conectedDevice)
                        self.grafico.show_graphic(self.conectedDevice)
                        self.connectButton.setEnabled(False)
                        self.disconnectButton.setEnabled(True)
                    except:
                        msg_box = QMessageBox(self)
                        msg_box.setText("Connection with the device failed. Check if another software is using the Tempico device or verify the hardware status.")
                        msg_box.setWindowTitle("Connection Error")
                        pixmap= QPixmap("/Sources/tausand_small.ico")
                        msg_box.setIconPixmap(pixmap)
                        msg_box.setIcon(QMessageBox.Critical)
                        msg_box.setStandardButtons(QMessageBox.Ok)
                        msg_box.exec_()

        else:
            openSentinel=False
            try:
                self.conectedDevice.open()
                self.LifeTimeTimer.start(500)
                openSentinel=True
            except:
                self.LifeTimeTimer.stop()
            if self.g2Graphic!=None and openSentinel:
                    self.g2Graphic.connectDevice()
            if self.LifeTimeGraphic!=None and openSentinel:
                    self.LifeTimeGraphic.connectedDevice(self.conectedDevice)
            if self.countsEstimatedGraphic!=None and openSentinel:
                    self.countsEstimatedGraphic.connectedDevice(self.conectedDevice)
            if self.timeStampGraphic!=None and openSentinel:
                    self.timeStampGraphic.connectedDevice(self.conectedDevice)
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)

    def disconnect_button_click(self):
        """
        Handles the disconnect button click event.

        This function hides the graphical display, disables the disconnect button, and re-enables the connect button.
        It also closes the connected device and resets its reference to `None`.
        If additional graphics like `g2Graphic` or `LifeTimeGraphic` are active, it will disconnect them as well.

        It does not take any parameters and does not return a value.
        :returns: None
        """
        if hasattr(self, 'grafico'):
            self.grafico.hide_graphic2()
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            self.conectedDevice.close()
            self.conectedDevice=None
        if self.g2Graphic!=None:
            self.g2Graphic.disconnectDevice()
        if self.LifeTimeGraphic!=None:
            self.LifeTimeGraphic.disconnectedDevice()
        if self.countsEstimatedGraphic!=None:
            self.countsEstimatedGraphic.disconnectedDevice()
        if self.timeStampGraphic!=None:
            self.timeStampGraphic.disconnectedDevice()




    #-----Functions for settings clicked--------#
    def clicked_tabs(self):
          """
          Executes an action when a tab is clicked and creates the corresponding window.

          This function checks which tab is currently active and constructs the associated window
          by invoking the appropriate function. If the tab corresponds to the Start/Stop Histogram,
          it stops the LifeTime timer and constructs the Start/Stop Histogram window. If the tab corresponds
          to the Lifetime Measurements, it constructs the Lifetime window and sets up the LifeTime logic if it
          has not been initialized yet.

          It does not take any parameters and does not return a value.
          :returns: None
          """
          valor_padre=self.tabs.currentIndex()
          padre=self.tab1
          if valor_padre==0:
              padre=self.tab1
              self.construct_start_stop_histogram(padre)
          elif valor_padre==1:
              padre=self.tab2
              self.construct_lifetime(padre)
              if self.LifeTimeGraphic==None:
                  #Get the data to create the logic class for LifeTime measurement
                  comboBoxStartChannel=self.uiLifeTime.startChannelComboBox
                  comboBoxStopChannel=self.uiLifeTime.stopChannelComboBox
                  graphicsFrame=self.uiLifeTime.graphicFrame
                  startButton=self.uiLifeTime.startButton
                  stopButton=self.uiLifeTime.stopButton
                  clearButton=self.uiLifeTime.clearButton
                  saveDataButton=self.uiLifeTime.saveDataFileButton
                  savePlotButton=self.uiLifeTime.savePlotButton
                  initialParametersButton=self.uiLifeTime.buttonParameterLabel
                  statusLabel=self.uiLifeTime.statusValue
                  pointLabel=self.uiLifeTime.drawPointLabel
                  comboBoxBinWidth=self.uiLifeTime.binWidthComboBox
                  spinBoxNumberMeasurements=self.uiLifeTime.numberMeasurementsSpinBox
                  totalTime=self.uiLifeTime.totalStopsValue
                  totalMeasurements=self.uiLifeTime.totalMeasurementsValue
                  totalStarts=self.uiLifeTime.totalStartsValue
                  applyButton=self.uiLifeTime.applyButtton
                  functionComboBox=self.uiLifeTime.functionComboBox
                  parametersTable=self.uiLifeTime.parametersTable
                  self.parametersTable=parametersTable
                  timeRange=self.uiLifeTime.timeRangeValue
                  numberBinsComboBox=self.uiLifeTime.numberBinsComboBox
                  self.LifeTimeGraphic=LifeTimeGraphic(comboBoxStartChannel, comboBoxStopChannel,graphicsFrame,startButton,stopButton,initialParametersButton,
                                               clearButton,saveDataButton,savePlotButton,statusLabel,pointLabel,comboBoxBinWidth,numberBinsComboBox,functionComboBox,
                                               spinBoxNumberMeasurements,totalMeasurements,totalStarts,totalTime,timeRange,self.conectedDevice,
                                               applyButton,parametersTable,self,self.LifeTimeTimer)
                  #If this sentinel dont have any use DELETE
                  self.LifeTime_init_sentinel=1
          elif valor_padre==2:
            padre=self.tab3
            self.construct_counts_estimated(padre)
            if self.countsEstimatedGraphic==None:
                #Get the data to create the logic class for Counts Estimated measurement
                channelACheckBox=self.uiCountsEstimated.channelACheckBox
                channelBCheckBox=self.uiCountsEstimated.channelBCheckBox
                channelCCheckBox=self.uiCountsEstimated.channelCCheckBox
                channelDCheckBox=self.uiCountsEstimated.channelDCheckBox
                startButon=self.uiCountsEstimated.startMeasurementButton
                stopButon=self.uiCountsEstimated.stopMeasurementButton
                mergeRadioButton=self.uiCountsEstimated.mergeGraphicButton
                separateRadioButton=self.uiCountsEstimated.separateGraphicButton
                deatachedRadioButton=self.uiCountsEstimated.apartDialogGraphicButton
                timeRangeComboBox=self.uiCountsEstimated.comboBoxTimeRange
                clearButtonChannelA=self.uiCountsEstimated.channelAClearButton
                clearButtonChannelB=self.uiCountsEstimated.channelBClearButton
                clearButtonChannelC=self.uiCountsEstimated.channelCClearButton
                clearButtonChannelD=self.uiCountsEstimated.channelDClearButton
                saveDataButtonCounts=self.uiCountsEstimated.saveDataButton
                savePlotButtonCounts=self.uiCountsEstimated.savePlotsButton
                channelACountValue=self.uiCountsEstimated.channelAValuesCount
                channelBCountValue=self.uiCountsEstimated.channelBValuesCount
                channelCCountValue=self.uiCountsEstimated.channelCValuesCount
                channelDCountValue=self.uiCountsEstimated.channelDValuesCount
                channelACountUncertainty=self.uiCountsEstimated.channelAUncertaintyCount
                channelBCountUncertainty=self.uiCountsEstimated.channelBUncertaintyCount
                channelCCountUncertainty=self.uiCountsEstimated.channelCUncertaintyCount
                channelDCountUncertainty=self.uiCountsEstimated.channelDUncertaintyCount
                #Frames for dinamic interface
                channelAFrameLabel=self.uiCountsEstimated.ChannelACountValues
                channelBFrameLabel=self.uiCountsEstimated.ChannelBCountValues
                channelCFrameLabel=self.uiCountsEstimated.ChannelCCountValues
                channelDFrameLabel=self.uiCountsEstimated.ChannelDCountValues

                tableCounts=self.uiCountsEstimated.countValuesTable
                graphicsFrame=self.uiCountsEstimated.GraphicsFrame
                statusLabel=self.uiCountsEstimated.labelState
                pointLabel=self.uiCountsEstimated.labelColor
                deatachedCheckBox=self.uiCountsEstimated.tableCheckBox
                detachedLabelCheckBox=self.uiCountsEstimated.labelCheckBox
                helpButton=self.uiCountsEstimated.helpButton
                self.countsEstimatedGraphic=CountEstimatedLogic(channelACheckBox,channelBCheckBox,channelCCheckBox,channelDCheckBox,startButon,stopButon,mergeRadioButton,separateRadioButton, deatachedRadioButton,timeRangeComboBox,clearButtonChannelA,clearButtonChannelB,clearButtonChannelC,clearButtonChannelD
                                                                ,saveDataButtonCounts,savePlotButtonCounts,channelACountValue,channelBCountValue,channelCCountValue,channelDCountValue, channelACountUncertainty,channelBCountUncertainty,channelCCountUncertainty,channelDCountUncertainty,tableCounts,graphicsFrame,channelAFrameLabel,channelBFrameLabel,channelCFrameLabel,channelDFrameLabel,statusLabel,pointLabel,deatachedCheckBox,detachedLabelCheckBox,helpButton,self.conectedDevice,self, self.LifeTimeTimer)
          elif valor_padre==3:
            padre=self.tab4
            self.construct_time_stamping(padre)  
            if self.timeStampGraphic==None:
                enableCheckBoxChannelA=self.uiTimeStamping.enableChannelACheckBox
                enableCheckBoxChannelB=self.uiTimeStamping.enableChannelBCheckBox
                enableCheckBoxChannelC=self.uiTimeStamping.enableChannelCCheckBox
                enableCheckBoxChannelD=self.uiTimeStamping.enableChannelDCheckBox
                scheduleCheckBox=self.uiTimeStamping.ScheduleMeasurementCheckBox
                scheduleTimeEdit=self.uiTimeStamping.scheduleDateTime
                limitMeasurementsCheckBox=self.uiTimeStamping.limitMeasurementsCheckBox
                limitMeasurementsSpinBox=self.uiTimeStamping.measurementsSpinBox
                showTableCheckBox= self.uiTimeStamping.showTableCheckBox
                syncComboBox= self.uiTimeStamping.syncComboBox
                startButtonTimeStamp= self.uiTimeStamping.startButton
                pauseButtonTimeStamp= self.uiTimeStamping.pauseButton
                stopButtonTimeStamp= self.uiTimeStamping.stopButton
                saveDataButtonTimeStamp=self.uiTimeStamping.saveDataButton
                valueMeasurementA=self.uiTimeStamping.label_7
                valueMeasurementB=self.uiTimeStamping.label_8
                valueMeasurementC=self.uiTimeStamping.label_9
                valueMeasurementD=self.uiTimeStamping.label_11
                valueMeasurementTotal=self.uiTimeStamping.label_10
                labelMeasurementsA=self.uiTimeStamping.label_4
                labelMeasurementsB=self.uiTimeStamping.label_2
                labelMeasurementsC=self.uiTimeStamping.label_5
                labelMeasurementsD=self.uiTimeStamping.label_3
                tableTimeStamp=self.uiTimeStamping.tableTimeStamp
                statusLabelTimeStamp=self.uiTimeStamping.valueStateLabel
                colorLabel=self.uiTimeStamping.labelColor
                self.timeStampGraphic=TimeStampLogic(enableCheckBoxChannelA,enableCheckBoxChannelB,enableCheckBoxChannelC,enableCheckBoxChannelD,scheduleCheckBox,scheduleTimeEdit,limitMeasurementsCheckBox,limitMeasurementsSpinBox,
                                                     showTableCheckBox, syncComboBox, startButtonTimeStamp, pauseButtonTimeStamp, stopButtonTimeStamp,saveDataButtonTimeStamp,valueMeasurementA,
                                                     valueMeasurementB, valueMeasurementC, valueMeasurementD, valueMeasurementTotal,labelMeasurementsA,labelMeasurementsB,labelMeasurementsC,labelMeasurementsD, tableTimeStamp, statusLabelTimeStamp, colorLabel,self,self.conectedDevice)
                

        #   elif valor_padre==1:

        #       padre=self.tab3
        #       self.construct_g2(padre)
        #       if self.g2Graphic ==None:
        #           comboBoxChannel1=self.uig2.Channel1ComboBox
        #           comboBoxChannel2=self.uig2.Channel2ComboBox
        #           graphicFrame=self.uig2.GraphicFrame
        #           HelpButton=self.uig2.HelpButton.clicked.connect(self.Helpg2Button)
        #           startButton=self.uig2.StartButton
        #           stopButton=self.uig2.StopButton
        #           saveDataButton=self.uig2.SaveDataButton
        #           savePlotButton=self.uig2.SavePlotButton
        #           N1Label=self.uig2.CountChannel1Value
        #           N2Label=self.uig2.CountChannel2Value
        #           LabelStatus=self.uig2.StatusValueMeasuremen
        #           PointStatus=self.uig2.StatusPoint
        #           comboBoxBin=self.uig2.BinWidthValue
        #           self.g2Graphic=g2Graphic(self,comboBoxChannel1,comboBoxChannel2,startButton,stopButton,saveDataButton,
        #                                    savePlotButton,N1Label,N2Label,LabelStatus,PointStatus,self.g2_init_sentinel,graphicFrame,comboBoxBin)
        #           self.g2_init_sentinel=1
        #       if self.initg2DialogSentinel==0:
        #         self.Helpg2Button()
        #         self.initg2DialogSentinel=1
        #Important when g2 is unified with LifeTime CHANGE THE INDEX TO 2


#The g2 functions are not use for the versions 1.1 comment for future versions

    def Helpg2Button(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("g2 measurement information")
        message_box.setStandardButtons(QMessageBox.Ok)
        custom_widget = QWidget()
        layout = QVBoxLayout(custom_widget)
        label = QLabel(custom_widget)
        layout.addWidget(label)
        pixmap = QPixmap('Sources/Help.png')

        pixmap = pixmap.scaledToWidth(700)
        label.setPixmap(pixmap)

        message_box.layout().addWidget(custom_widget)


        message_box.exec_()



    def settings_clicked(self):
        """
        Opens the settings window when the settings option is clicked.

        This function checks if a device is connected. If no measurement is currently running,
        it displays the settings window for channel configuration. If a measurement is running,
        a message box is shown informing the user that changes cannot be made while a measurement
        is in progress. If no device is connected, a message box alerts the user that no device
        was found.

        It does not take any parameters and does not return a value.
        :returns: None
        """
        if self.conectedDevice!=None:
            if not self.currentMeasurement:
                self.dialog_settings=QDialog(self)
                self.settings_channels = Ui_settings()
                self.settings_channels.setupUi(self.dialog_settings, self.conectedDevice)
                self.settings_channels.get_settings()
                self.dialog_settings.exec_()
                self.openSettings=True
            else:
                #Open warning dialog
                message_box = QMessageBox(self)
                message_box.setWindowTitle("Running measurement")
                message_box.setText("The measurement is running, the settings only can be read. Changes cannot be made while a measurement is in progress.")
                pixmap= QPixmap(ICON_LOCATION)
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Information)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
                #Open settings
                self.dialog_settings=QDialog(self)
                self.settings_channels = Ui_settings()
                self.settings_channels.setupUi(self.dialog_settings, self.conectedDevice)
                self.settings_channels.preDefinedSettings(self.averageCycleChannelA,self.averageCycleChannelB,self.averageCycleChannelC,self.averageCycleChannelD,
                                                            self.modeChangeChannelA,self.modeChangeChannelB,self.modeChangeChannelC,self.modeChangeChannelD,
                                                            self.numberOfStopsChannelA,self.numberOfStopsChannelB,self.numberOfStopsChannelC,self.numberOfStopsChannelD,
                                                            self.edgeTypeChannelA,self.edgeTypeChannelB,self.edgeTypeChannelC,self.edgeTypeChannelD,
                                                            self.stopMaskChannelA,self.stopMaskChannelB,self.stopMaskChannelC,self.stopMaskChannelD)
                self.settings_channels.onlyReading()
                self.dialog_settings.exec_()




        else:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("No connected device")
            message_box.setText("No connected device was found")
            pixmap= QPixmap(ICON_LOCATION)
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()

    def enableSettings(self):
        """
        Re-enables the device and general settings dialogs if they are open.

        If either the device configuration or general settings dialog is currently visible,
        this function refreshes and reactivates their interactive fields by calling the
        corresponding `get_settings()` and `enableSettings()` methods.

        :return: None
        """
        if self.openSettings:
            if self.dialog_settings.isVisible():
                self.settings_channels.get_settings()
                self.settings_channels.enableSettings()
        if self.openGeneralSettings:
            if self.settings_windows.isVisible():
                self.settings_windows.getsettings()
                self.settings_windows.enableSettings()


    def saveSettings(self):
        """
        Retrieves and stores the current device configuration into internal variables.

        This function queries the connected device for channel-specific settings such as
        averaging cycles, mode, number of stops, stop edge type, stop mask, threshold voltage,
        and number of runs. These values are saved into instance attributes for later use,
        such as restoring settings or displaying them in the UI.

        :return: None
        """
        if self.conectedDevice!=None:
            #Get the channels objects
            channel1=self.conectedDevice.ch1
            channel2=self.conectedDevice.ch2
            channel3=self.conectedDevice.ch3
            channel4=self.conectedDevice.ch4
            #Get the average cycles
            self.averageCycleChannelA=int(math.log(channel1.getAverageCycles(),2))
            self.averageCycleChannelB=int(math.log(channel2.getAverageCycles(),2))
            self.averageCycleChannelC=int(math.log(channel3.getAverageCycles(),2))
            self.averageCycleChannelD=int(math.log(channel4.getAverageCycles(),2))
            #Get the mode
            self.modeChangeChannelA=channel1.getMode()
            self.modeChangeChannelB=channel2.getMode()
            self.modeChangeChannelC=channel3.getMode()
            self.modeChangeChannelD=channel4.getMode()
            #Get the number of stops
            self.numberOfStopsChannelA=channel1.getNumberOfStops()
            self.numberOfStopsChannelB=channel2.getNumberOfStops()
            self.numberOfStopsChannelC=channel3.getNumberOfStops()
            self.numberOfStopsChannelD=channel4.getNumberOfStops()
            #Get and transform the stop edge
            self.edgeTypeChannelA=channel1.getStopEdge()
            if (self.edgeTypeChannelA=="RISE"):
                self.edgeTypeChannelA=0
            else:
                self.edgeTypeChannelA=1

            self.edgeTypeChannelB=channel2.getStopEdge()
            if (self.edgeTypeChannelB=="RISE"):
                self.edgeTypeChannelB=0
            else:
                self.edgeTypeChannelB=1

            self.edgeTypeChannelC=channel3.getStopEdge()
            if (self.edgeTypeChannelC=="RISE"):
                self.edgeTypeChannelC=0
            else:
                self.edgeTypeChannelC=1

            self.edgeTypeChannelD=channel4.getStopEdge()
            if (self.edgeTypeChannelD=="RISE"):
                self.edgeTypeChannelD=0
            else:
                self.edgeTypeChannelD=1
            #Get the stop mask
            self.stopMaskChannelA=int(channel1.getStopMask())
            self.stopMaskChannelB=int(channel2.getStopMask())
            self.stopMaskChannelC=int(channel3.getStopMask())
            self.stopMaskChannelD=int(channel4.getStopMask())
            #Get the threshold voltage
            self.thresholdVoltage=self.conectedDevice.getThresholdVoltage()
            self.numberRuns=self.conectedDevice.getNumberOfRuns()







    def general_settings_clicked(self):
        """
        Opens the general settings window for device-wide configurations.

        This function checks if a device is connected. If no measurement is currently running,
        it opens the general settings window where configurations that affect the entire device
        (regardless of the channel) can be adjusted. If a measurement is running, a message box
        is displayed to inform the user that changes cannot be made while the measurement is in
        progress. If no device is connected, a message box is shown indicating that no device was found.

        It does not take any parameters and does not return a value.
        :returns: None
        """
        if self.conectedDevice!=None:
            if not self.currentMeasurement:
                self.settings_windows=GeneralSettingsWindow(self.conectedDevice)
                self.settings_windows.getsettings()
                self.openGeneralSettings=True
                self.settings_windows.exec_()

            else:
                message_box = QMessageBox(self)  # Icono de advertencia
                message_box.setWindowTitle("Running measurement")
                message_box.setText("The measurement is running, the settings only can be read. Changes cannot be made while a measurement is in progress.")
                pixmap= QPixmap(ICON_LOCATION)
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Information)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
                self.settings_windows=GeneralSettingsWindow(self.conectedDevice)
                self.settings_windows.preDefinedSettings(self.thresholdVoltage, self.numberRuns)
                self.settings_windows.disableSettings()
                self.openGeneralSettings=True
                self.settings_windows.exec_()


        else:
            message_box = QMessageBox(self)  # Icono de advertencia
            message_box.setWindowTitle("No connected device ")
            message_box.setText("No connected device was found")
            pixmap= QPixmap(ICON_LOCATION)
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()



    def about_settings(self):
        """
        Opens the About window displaying information about the company, version, and repository.

        This function opens a window showing details about the company (Tausand), the software version,
        and the location of the repository. It does not perform any checks or validations and directly
        displays the About window.

        It does not take any parameters and does not return a value.
        :returns: None
        """

        settings_windows_dialog=QDialog(self)
        settings_windows=Ui_AboutDialog()
        settings_windows.setupUi(settings_windows_dialog)
        settings_windows_dialog.exec_()


#This function is not use for the Tempico Version 1.1
#TO DO: Comment the function for a future version
    def parameters_action(self):
        if self.conectedDevice!=None:
            if not self.currentMeasurement:
                self.dialogParameters=QDialog(self)
                self.uiParameter = UiParameters()
                self.uiParameter.setupUi(self.dialogParameters)
                if self.g2Graphic!=None:
                    self.g2Graphic.timerStatus.stop()
                self.parametersLogic=CountParameters(self.uiParameter.channelComboBox,self.conectedDevice,self.uiParameter.measurementLabel,
                                                     self.uiParameter.measuremetStatusLabel,self.uiParameter.informationMeasureLabel,
                                                     self.uiParameter.startButton,self.uiParameter.stopButton,self.dialogParameters, self.g2Graphic,self)
                self.dialogParameters.exec_()
            else:
                message_box = QMessageBox(self)
                message_box.setWindowTitle("Running measurement")
                message_box.setText("It is not possible to make changes when a measurement is running.")
                pixmap= QPixmap(ICON_LOCATION)
                message_box.setIconPixmap(pixmap)
                message_box.setIcon(QMessageBox.Information)
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()

        else:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("No connected Device ")
            message_box.setText("No connected device was found")
            pixmap= QPixmap(ICON_LOCATION)
            message_box.setIconPixmap(pixmap)
            message_box.setIcon(QMessageBox.Information)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()

        pass

    def closeEvent(self, event):
        """
        Handles the close event of the main window and prompts the user for confirmation.

        This function is triggered when the user attempts to close the main window. It displays
        a dialog asking if the user is sure about closing the application (Tempico software).
        If the user confirms by selecting "Yes", the event is accepted and the application closes.
        If the user selects "No", the close event is ignored, and the application remains open.

        :param event: The close event triggered when attempting to close the window.
        :type event: QCloseEvent
        :returns: None
        """
        reply = QMessageBox.question(self, 'Exit',
            "Are you sure you want to close tempico software?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    #Resize the graphics
    def resizeEvent(self,event):
        """
        Handles the window resize event and adjusts the column widths of the parameters table.

        This function is triggered when the user resizes the main window. It resizes the columns
        of the parameters table in the LifeTime tab based on the current window width. The column
        widths are scaled proportionally to ensure the table adapts to the new window size.

        :param event: The resize event triggered when the window is resized.
        :type event: QResizeEvent
        :returns: None
        """
        if self.LifeTimeGraphic!=None:
            currentValue=self.width()
            self.parametersTable.setColumnWidth(0, int(round(currentValue*1/50)))
            self.parametersTable.setColumnWidth(1, int(round(currentValue*1/10)))
            self.parametersTable.setColumnWidth(2, int(round(currentValue*1/10)))
            self.parametersTable.setColumnWidth(3, int(round(currentValue*1/50)))

    def manageConection(self):
        """
        Manages the connection status with the measurement device.

        This function checks if the device is still connected. If the connection is lost, it stops the
        timer responsible for monitoring the device, removes the device instance, disables measurement
        functionalities in all tabs, and displays an error dialog to inform the user.

        :return: None
        """
        if self.conectedDevice:
            try:
                self.conectedDevice.readIdnFromDevice()
            except:
                if self.countsEstimatedGraphic:
                    self.countsEstimatedGraphic.disconnectedDevice()
                if self.timeStampGraphic:
                    self.timeStampGraphic.disconnectedDevice()
                if self.LifeTimeGraphic:
                    self.LifeTimeGraphic.disconnectedDevice()
                if self.grafico:
                    self.grafico.disconnectedDevice()
                self.LifeTimeTimer.stop()
                self.conectedDevice=None
                msg_box = QMessageBox(self)
                msg_box.setText("Connection with the device has been lost")
                msg_box.setWindowTitle("Connection Error")
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

    def disconnectedDevice(self):
        """
        Handles device disconnection without displaying any user interface dialogs.

        This function is triggered when the connection with the device is lost. It notifies
        all relevant components to handle the disconnection and sets the connected device
        reference to None.

        :return: None
        """
        if self.countsEstimatedGraphic:
            self.countsEstimatedGraphic.disconnectedDevice()
        if self.timeStampGraphic:
            self.timeStampGraphic.disconnectedDevice()
        if self.LifeTimeGraphic:
            self.LifeTimeGraphic.disconnectedDevice()
        if self.grafico:
            self.grafico.disconnectedDevice()
        self.conectedDevice=None

    #Function to advise that a measurement is active
    def activeMeasurement(self):
        """
        Activates the sentinel indicating that a measurement is currently running.

        This function sets the internal flag to True, which is used to track the
        active state of a measurement process.

        :return: None
        """
        self.currentMeasurement=True

    #Function to advise that a measurement is finished
    def noMeasurement(self):
        """
        Deactivates the sentinel indicating that no measurement is currently running.

        This function sets the internal flag to False, marking that there is no active
        measurement process at the moment.

        :return: None
        """
        self.currentMeasurement=False







#--------Execution Test----------#

if __name__ == '__main__':
    app = QApplication([])
    #Amber theme
    #apply_stylesheet(app, theme='dark_amber.xml')
    #Amber purple
    # apply_stylesheet(app, theme='light_purple_500.xml')
    # app.setStyleSheet(app.styleSheet() + """
    # /* Aplica solo a QPushButton dentro de QWidget para tener prioridad */
    # QWidget QPushButton {
    #     color: #4a0072;
    #     font-weight: bold;
    # }

    # /* Hover elegante con fondo morado claro */
    # QWidget QPushButton:hover {
    #     background-color: #f3e5f5;
    #     border: 1px solid #ce93d8;
    # }

    # /* Botones deshabilitados con texto legible */
    # QWidget QPushButton:disabled {
    #     color: #888888;
    #     background-color: #f5f5f5;
    #     border: 1px solid #dddddd;
    # }
    # """)
    splash_pix = QPixmap(BANNER)
    desired_size = QSize(400, 300)
    splash_pix = splash_pix.scaled(desired_size, Qt.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setFixedSize(desired_size)
    # Comprobar si estamos en Ubuntu
    if sys.platform != 'linux':  # Si no estamos en Ubuntu, aplicar opacidad
        opaqueness = 0.0
        step = 0.1
        splash.setWindowOpacity(opaqueness)

        while opaqueness < 1:
            splash.setWindowOpacity(opaqueness)
            time.sleep(step)
            opaqueness += step

        splash.show()
        time.sleep(1)  # Mostrar splash por 1 segundo
        splash.close()
        window = MainWindow()
        window.show()
    else:
        splash.show()
        time.sleep(1)
        splash.close()
        window = MainWindow()
        window.show()

    app.exec_()

def execProgram():
    app = QApplication([])
    splash_pix = QPixmap(BANNER)
    desired_size = QSize(400, 300)
    splash_pix = splash_pix.scaled(desired_size, Qt.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setFixedSize(desired_size)
    opaqueness = 0.0
    step = 0.1
    splash.setWindowOpacity(opaqueness)
    splash.show()

    while opaqueness < 1:
        splash.setWindowOpacity(opaqueness)
        time.sleep(step)
        opaqueness += step

    time.sleep(1)
    splash.close()
    window = MainWindow()
    window.show()
    app.exec_()

