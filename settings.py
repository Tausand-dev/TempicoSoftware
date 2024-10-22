#No utilizado (To do: revisar cosas utiles y posteriormente eliminar)


from PySide2.QtWidgets import QDialog, QLabel, QCheckBox, QTabWidget, QWidget, QComboBox, QSpinBox
from PySide2.QtGui import QIcon



class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Channels settings")
        self.setFixedSize(400,240)
        self.setWindowIcon(QIcon('Sources/tausand_small.ico'))
        #----------construct enable channel----------#
        self.sentinel1=0
        self.sentinel2=0
        self.sentinel3=0   
        self.sentinel4=0
        self.channelsLabel=QLabel("Enable/disable channels:",self)
        self.channelsLabel.setGeometry(65,10,150,20)
        self.checkchannelA = QCheckBox("A",self)
        self.checkchannelB = QCheckBox("B",self)
        self.checkchannelC = QCheckBox("C",self)
        self.checkchannelD = QCheckBox("D",self)
        self.checkchannelA.setChecked(True)
        self.checkchannelB.setChecked(True)
        self.checkchannelC.setChecked(True)
        self.checkchannelD.setChecked(True)
        self.channelvalueA=1
        self.channelvalueB=1
        self.channelvalueC=1
        self.channelvalueD=1
        self.checkchannelA.toggled.connect(self.clicked_channelA)
        self.checkchannelB.toggled.connect(self.clicked_channelB)
        self.checkchannelC.toggled.connect(self.clicked_channelC)
        self.checkchannelD.toggled.connect(self.clicked_channelD)
        self.checkchannelA.setGeometry(210,10,50,20)
        self.checkchannelB.setGeometry(240,10,50,20)
        self.checkchannelC.setGeometry(270,10,50,20)
        self.checkchannelD.setGeometry(300,10,50,20)
        

        #-----------Create a qtabwidget for every channel-----------------#
        self.tabs=QTabWidget(self)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tab4=QWidget()
        self.tabs.addTab(self.tab1,"ChannelA")
        self.tabs.addTab(self.tab2,"ChannelB")
        self.tabs.addTab(self.tab3,"ChannelC")
        self.tabs.addTab(self.tab4,"ChannelD")
        self.tabs.currentChanged.connect(self.clicked_tab1)
        self.tabs.setGeometry(0,40,400,250)
        #We establish as default the channel A to be open

        #-----------Construct the settings-----------------#
        self.construc_settings_option(0)
        self.construc_settings_option(1)
        self.construc_settings_option(2)
        self.construc_settings_option(3)
        
        




       

    #---------Function to construct the settings window-------#
    def construc_settings_option(self,index):
        
        if index==0:
             parent=self.tab1
        elif index==1:
             parent=self.tab2
        elif index==2:
             parent=self.tab3
        elif index==3:
             parent=self.tab4
     
        

        if (index==0 and self.sentinel1==0) or (index==1 and self.sentinel2==0) or (index==2 and self.sentinel3==0) or (index==3 and self.sentinel4==0):
          
          if index==0:
              parent=self.tab1
          elif index==1:
             parent=self.tab2
          elif index==2:
             parent=self.tab3
          elif index==3:
             parent=self.tab4
          

          #---------------Average cycles channels-------------------#


          
          self.cyclesvaluesLabel=QLabel(" Average cycles: ",parent)
          self.cyclesvaluesLabel.setGeometry(70,10,150,20)
          self.ComboboxCycles=QComboBox(parent)
          self.ComboboxCycles.addItems(["1","2","4","8","16","32","64","128"])
          self.ComboboxCycles.setGeometry(180,10,100,20)
          



          #---------------Channel modes-------------------#
     
          self.ModeLabel=QLabel(" Mode: ",parent)
          self.ModeLabel.setGeometry(70,40,150,20)
          self.ComboboxChannelsModes=QComboBox(parent)
          self.ComboboxChannelsModes.addItems(["Mode 1 range: 12ns to 500ns","Mode 2 range: 125ns to 4ms"])
          self.ComboboxChannelsModes.setGeometry(180,40,200,20)

          #---------------Number of stops-------------------#
          
          self.StopsLabel=QLabel("Number of stops: ",parent)
          self.StopsLabel.setGeometry(70,70,150,20)
          self.ComboboxChannelsStops=QComboBox(parent)
          self.ComboboxChannelsStops.addItems(["1","2","3","4","5"])
          self.ComboboxChannelsStops.setGeometry(180,70,50,20)
          #---------------Edge-------------------#
          
          self.EdgeTypeLabel=QLabel("Edge Type: ",parent)
          self.EdgeTypeLabel.setGeometry(70,100,150,20)
          self.ComboboxChannelsEdgeType=QComboBox(parent)
          self.ComboboxChannelsEdgeType.addItems(["RISE","FALL"])
          self.ComboboxChannelsEdgeType.setGeometry(180,100,50,20)
          #---------------Stop Mask-------------------#
          
          self.StopMaskvaluesLabel=QLabel(" Stop Mask: ",parent)
          self.StopMaskvaluesLabel.setGeometry(70,130,150,20)
          self.spinboxStopMask = QSpinBox(parent)
          self.spinboxStopMask.setMinimum(0)  # Valor mínimo permitido
          self.spinboxStopMask.setMaximum(4000)  # Valor máximo permitido
          self.spinboxStopMask.setSingleStep(1)  # Incremento/decremento en 1
          self.spinboxStopMask.setWrapping(True)  # Volver al valor mínimo después del valor máximo
          self.spinboxStopMask.setButtonSymbols(QSpinBox.PlusMinus)  # Mostrar botones de más/menos
          self.spinboxStopMask.setAccelerated(True)  # Acelerar la velocidad del aumento/decremento
          self.spinboxStopMask.setGeometry(180,130,100,20)
          self.spinboxStopMask.setSuffix(" "+ "μs")
          if index==0:
              self.sentinel1=1
          elif index==1:
              self.sentinel2=1
          elif index==2:
              self.sentinel3=1
          elif index==3:
              self.sentinel4=1

    #---------Update tab parent-------#
    def clicked_tab1(self):
          valor_padre=self.tabs.currentIndex()
          self.construc_settings_option(valor_padre)       


    #---------Update values checkboxes-------#
    def clicked_channelA(self):
        if self.checkchannelA.isChecked():
             self.channelvalueA=1
        else:
             self.channelvalueA=0     
        

    def clicked_channelB(self):
        if self.checkchannelB.isChecked():
             self.channelvalueB=1
        else:
             self.channelvalueB=0
        
        
    def clicked_channelC(self):
        if self.checkchannelC.isChecked():
             self.channelvalueC=1
        else:
             self.channelvalueC=0
        

    def clicked_channelD(self):
        if self.checkchannelD.isChecked():
             self.channelvalueD=1
        else:
             self.channelvalueD=0
