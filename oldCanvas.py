#File created in order to save the last version of canvas class
#TO DO DELETE FILE
from PySide2.QtCore import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
from PySide2.QtWidgets import QWidget, QTabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import datetime as dt
import numpy as np
import pyTempico as tempico
import pyAbacus as abacus
from settings import SettingsWindow
from generalsettings import GeneralSettingsWindow
from aboutWindow import AboutWindow
from StartStopHistograms import StartStopHistogramsWindow as SSHistogramsWindow
from ui_StarStopHistogram import Ui_HistogramaStartStop
from ui_lifetime import Ui_Form
from ui_g2measurement import Ui_G2
from ui_devicesDialog import Ui_Devices
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide2.QtCore import QTimer
#To do eliminate import
import random
import createsavefile as savefile
import datetime
from ui_settings import Ui_settings

class Canvas():
    def __init__(self, parent, valor,device,check1,check2,check3,check4,startbutton,stopbutton,savebutton,save_graph_1,save_graph_2,clear_channel_A,clear_channel_B,clear_channel_C,clear_channel_D, *args, **kwargs):
        super().__init__()
        #Current measurement
        self.currentmeasurement=False
        
        ##----------------##
        self.startbutton=startbutton
        self.stopbutton=stopbutton
        self.savebutton=savebutton
        self.save_graph_1=save_graph_1
        self.save_graph_2=save_graph_2
        self.clear_channel_A=clear_channel_A
        self.clear_channel_B=clear_channel_B
        self.clear_channel_C=clear_channel_C
        self.clear_channel_D=clear_channel_D
        #Disable buttons init
        self.savebutton.setEnabled(False)
        self.stopbutton.setEnabled(False)
        self.save_graph_1.setEnabled(False)
        self.save_graph_2.setEnabled(False)
        self.clear_channel_A.setEnabled(False)
        self.clear_channel_B.setEnabled(False)
        self.clear_channel_C.setEnabled(False)
        self.clear_channel_D.setEnabled(False)
        ##---------------------------------##
        ##---------------------------------##
        ##--------Begin graphic ms --------##
        ##---------------------------------##
        ##---------------------------------##
        self.win=pg.GraphicsLayoutWidget()
        
        self.win.setBackground('w')
        self.parent=parent
        #Creating the histogram plot channel A
        self.data=[]
        self.hist, self.bins=np.histogram(self.data,bins=60)
        #Creating the histogram plot channel B
        self.dataB=[]
        self.histB, self.binsB=np.histogram(self.dataB,bins=60)
        #Creating the histogram plot channel C
        self.dataC=[]
        self.histC, self.binsC=np.histogram(self.dataC,bins=60)
        #Creating the histogram plot channel D
        self.dataD=[]
        self.histD, self.binsD=np.histogram(self.dataD,bins=60)
        
        #Pure data
        self.datapureA=[]
        self.datapureB=[]
        self.datapureC=[]
        self.datapureD=[]
        
        self.plot=self.win.addPlot()
        self.plot.showGrid(x=True,y=True)
        ##---------------------------------##
        ##---------------------------------##
        ##--------End graphic ms ----------##
        ##---------------------------------##
        ##---------------------------------##
        
        
        
        

        #Get the channels
        self.device=device
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        #-----------------#
        
        self.legend = self.plot.addLegend()
        
        
        self.plot.setTitle('Start-Stop Histogram')
        self.plot.setLabel('left','Frequency')
        self.plot.setLabel('bottom','Values(ms)')
        self.verticalLayout=QVBoxLayout(self.parent)
        self.verticalLayout.addWidget(self.win)
        self.plot.setXRange(0, 5)
        
        ##---------------------------------##
        ##---------------------------------##
        ##--------Begin graphic ns --------##
        ##---------------------------------##
        ##---------------------------------##
        
        self.win_ns=pg.GraphicsLayoutWidget()
        self.win_ns.setBackground('w')
        self.parent=parent
        #Creating the histogram plot channel A
        self.plot_ns=self.win_ns.addPlot()
        self.plot_ns.showGrid(x=True,y=True)
        self.plot_ns.setTitle('Start-Stop Histogram')
        self.plot_ns.setLabel('left','Frequency')
        self.plot_ns.setLabel('bottom','Values(ns)')
        self.verticalLayout.addWidget(self.win_ns)
        
        
        
        ##---------------------------------##
        ##---------------------------------##
        ##--------End graphic ns ----------##
        ##---------------------------------##
        ##---------------------------------##

        
        
        #Legends labels#
        self.legend_ns = self.plot_ns.addLegend()
        self.graphic_ms_ns()
        
        #-------------#
        

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(3000)
        self.startbutton.clicked.connect(self.start_graphic)
        self.stopbutton.clicked.connect(self.stop_graphic)
        self.savebutton.clicked.connect(self.save_graphic)
        self.clear_channel_A.clicked.connect(self.clear_a)
        self.clear_channel_B.clicked.connect(self.clear_b)
        self.clear_channel_C.clicked.connect(self.clear_c)
        self.clear_channel_D.clicked.connect(self.clear_d)
        self.save_graph_1.clicked.connect(self.save_plot_ms)
        self.save_graph_2.clicked.connect(self.save_plot_ns)
        #We define here the variables of the histogram window
        self.checkA=check1 
        self.checkB=check2
        self.checkC=check3
        self.checkD=check4
        self.sentinel=False
        self.plot.setMouseEnabled(x=True, y=False)
        self.plot_ns.setMouseEnabled(x=True, y=False)
        #Iterator in order to avoid the warning alert from pyqt5
        self.channelA_enable=True
        self.channelA_disabled=False
        self.channelB_enable=True
        self.channelB_disabled=False
        self.channelC_enable=True
        self.channelC_disabled=False
        self.channelD_enable=True
        self.channelD_disabled=False
        self.plot_ns.setXRange(0, 500)
        
        #Define the label
        self.units_A='ms'
        self.units_B='ms'
        self.units_C='ms'
        self.units_D='ms'
        self.viewbox = self.plot.getViewBox()
        self.viewbox.sigRangeChanged.connect(self.zoom_changed)
        self.viewbox2 = self.plot_ns.getViewBox()
        self.viewbox2.sigRangeChanged.connect(self.zoom_changed2)
        self.sentinelsave=0
        self.oldroute=""
        
        
        
    #Start taking data with the start button    
    def start_graphic(self):
        
        self.currentmeasurement=True
        self.sentinelsave=0
        self.new_start()
        if self.checkA.isChecked():
            self.channelA_disabled=True
            self.channelA_enable=False
        if self.checkB.isChecked():
            self.channelB_disabled=True
            self.channelB_enable=False
        if self.checkC.isChecked():
            self.channelC_disabled=True
            self.channelC_enable=False
        if self.checkD.isChecked():
            self.channelD_disabled=True
            self.channelD_enable=False
        self.graphics_channels()
        self.graphics_channels_B()
        self.graphics_channels_C()
        self.graphics_channels_D()
        self.sentinel=True
        self.data=[]
        self.dataB=[]
        self.dataC=[]
        self.dataD=[]
        self.savebutton.setEnabled(False)
        self.startbutton.setEnabled(False)
        self.stopbutton.setEnabled(True)
        self.clear_channel_A.setEnabled(True)
        self.clear_channel_B.setEnabled(True)
        self.clear_channel_C.setEnabled(True)
        self.clear_channel_D.setEnabled(True)

    #Stop taking data with stop button
    def stop_graphic(self):
        self.currentmeasurement=False
        self.sentinel=False
        self.stopbutton.setEnabled(False)
        self.startbutton.setEnabled(True)
        self.savebutton.setEnabled(True)
        self.save_graph_1.setEnabled(True)
        self.save_graph_2.setEnabled(True)
    
    #Clear the data from the graphics
    def clear_a(self):
        self.data=[]
        
    def clear_b(self):
        self.dataB=[]
    
    def clear_c(self):
        self.dataC=[]
    
    def clear_d(self):
        self.dataD=[]
    
    #Save plot images
    def save_plot_ms(self):
        try:
            exporter= pg.exporters.ImageExporter(self.plot)
            exporter.parameters()['width'] = 800
            exporter.parameters()['height'] = 600
            folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
            current_date=datetime.datetime.now()
            current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            graph_name='Measure_ms'+current_date_str
            exporter.export(folder_path+'\\'+graph_name+'.png')
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Information)
            message_box.setText("The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+graph_name)
            message_box.setWindowTitle("Successful save")
            message_box.setStandardButtons(QMessageBox.Ok)

            # Mostrar el QMessageBox y esperar a que el usuario lo cierre
            message_box.exec_()
        except:
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
    
    def save_plot_ns(self):
        try:
            
            exporter= pg.exporters.ImageExporter(self.plot_ns)
            exporter.parameters()['width'] = 800
            exporter.parameters()['height'] = 600
            folder_path=savefile.read_default_data()['Folder path'].replace('\n', '')
            current_date=datetime.datetime.now()
            current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            graph_name='Measure_ns'+current_date_str
            exporter.export(folder_path+'\\'+graph_name+'.png')
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Information)
            message_box.setText("The plots have been saved successfully in "+"\n"+ str(folder_path)+"\n"+graph_name)
            message_box.setWindowTitle("Successful save")
            message_box.setStandardButtons(QMessageBox.Ok)

            # Mostrar el QMessageBox y esperar a que el usuario lo cierre
            message_box.exec_()
        except:
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("The plots could not be saved.")
            message_box.setWindowTitle("Error saving")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            
    
    
    
    #Save the graphic in a file
    def save_graphic(self):
        if self.sentinelsave==0:
            data_prefix=savefile.read_default_data()['Default Histogram Name']
            current_date=datetime.datetime.now()
            current_date_str=current_date.strftime("%Y-%m-%d %H:%M:%S").replace(':','').replace('-','').replace(' ','')
            filename1=data_prefix+current_date_str+'channel1'
            filename2=data_prefix+current_date_str+'channel2'
            filename3=data_prefix+current_date_str+'channel3'
            filename4=data_prefix+current_date_str+'channel4'
            setting_A="Average cycles: "+str(self.channel1.getAverageCycles())+ "\nMode: "+str(self.channel1.getMode())+"\nNumber of stops:"+ str(self.channel1.getNumberOfStops())+"\nStop edge: "+str(self.channel1.getStopEdge())+ "\nStop mask: "+str(self.channel1.getStopMask())
            setting_B="Average cycles: "+str(self.channel2.getAverageCycles())+ "\nMode: "+str(self.channel2.getMode())+"\nNumber of stops:"+ str(self.channel2.getNumberOfStops())+"\nStop edge: "+str(self.channel2.getStopEdge())+ "\nStop mask: "+str(self.channel2.getStopMask())
            setting_C="Average cycles: "+str(self.channel3.getAverageCycles())+ "\nMode: "+str(self.channel3.getMode())+"\nNumber of stops:"+ str(self.channel3.getNumberOfStops())+"\nStop edge: "+str(self.channel3.getStopEdge())+ "\nStop mask: "+str(self.channel3.getStopMask())
            setting_D="Average cycles: "+str(self.channel4.getAverageCycles())+ "\nMode: "+str(self.channel4.getMode())+"\nNumber of stops:"+ str(self.channel4.getNumberOfStops())+"\nStop edge: "+str(self.channel4.getStopEdge())+ "\nStop mask: "+str(self.channel4.getStopMask())
            settings=[setting_A,setting_B,setting_C,setting_D]
            folder_path=savefile.read_default_data()['Folder path']
            filenames=[filename1,filename2,filename3,filename4]
            data=[self.datapureA,self.datapureB,self.datapureC,self.datapureD]
            column_names=['channel1_data (ps)','channel2_data (ps)','channel3_data (ps)','channel4_data (ps)']
            try:
                savefile.save_lists_as_columns_txt(data,filenames,column_names,folder_path,settings)
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Information)
                message_box.setText("The files have been saved successfully in path folder: "+"\n\n"+ str(folder_path)+"\n\n"+"with the following names:"+"\n\n"+"File1: "+filename1+".txt"+'\n\n'+"File2: "+filename2+".txt"+'\n\n'+"File3: "+filename3+".txt"+'\n\n'+"File4: "+filename4+".txt")
                self.oldroute="The files have already been saved in path folder: "+"\n\n"+ str(folder_path)+"\n\n"+"with the following names:"+"\n\n"+"File1: "+filename1+".txt"+'\n\n'+"File2: "+filename2+".txt"+'\n\n'+"File3: "+filename3+".txt"+'\n\n'+"File4: "+filename4+".txt"
                message_box.setWindowTitle("Successful save")
                message_box.setStandardButtons(QMessageBox.Ok)

                message_box.exec_()
            except:
                #If an error occurs, an error message box will be displayed.
                message_box = QMessageBox(self.parent)
                message_box.setIcon(QMessageBox.Critical)
                message_box.setText("The changes could not be saved.")
                message_box.setWindowTitle("Error saving")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            self.savebutton.setEnabled(True)
            self.sentinelsave=1
        else:
            message_box = QMessageBox(self.parent)
            message_box.setIcon(QMessageBox.Information)
            message_box.setText(self.oldroute)
            message_box.setWindowTitle("Successful save")
            message_box.setStandardButtons(QMessageBox.Ok)

            message_box.exec_()
            
        
        
        
    
    #Removing or adding the graphics to the widget when the checkbox is marked
    def graphics_channels(self):
        #Check the channel A
        mode_A=self.channel1.getMode()
        if not self.checkA.isChecked() and not self.channelA_disabled:
            
            if mode_A==2:
                print("Se retira la grafica de A")
                self.plot.removeItem(self.curve)
            else:
                self.plot_ns.removeItem(self.curve)
            self.channelA_enable=False
            self.channelA_disabled=True
            
        if self.checkA.isChecked() and not self.channelA_enable:
            if mode_A==2:
                self.plot_ns.removeItem(self.curve)
                self.plot.addItem(self.curve)
            else:
                self.plot.removeItem(self.curve)
                self.plot_ns.addItem(self.curve)
            self.channelA_enable=True 
            self.channelA_disabled=False

    def graphics_channels_B(self):
        mode_B=self.channel2.getMode()
        if not self.checkB.isChecked() and not self.channelB_disabled:
            if mode_B==2:
                self.plot.removeItem(self.curveB)
            else:
                self.plot_ns.removeItem(self.curveB)
            self.channelB_enable=False
            self.channelB_disabled=True
            
        if self.checkB.isChecked() and not self.channelB_enable:
            if mode_B==2:
                self.plot_ns.removeItem(self.curveB)
                self.plot.addItem(self.curveB)
            else:
                self.plot.removeItem(self.curveB)
                self.plot_ns.addItem(self.curveB)
            self.channelB_enable=True 
            self.channelB_disabled=False
            
    def graphics_channels_C(self):
        #Check the channel C
        mode_C=self.channel3.getMode()
        if not self.checkC.isChecked() and not self.channelC_disabled:
            if mode_C==2:
                self.plot.removeItem(self.curveC)
            else:
                self.plot_ns.removeItem(self.curveC)
            self.channelC_enable=False
            self.channelC_disabled=True
            
        if self.checkC.isChecked() and not self.channelC_enable:
            if mode_C==2:
                self.plot_ns.removeItem(self.curveC)
                self.plot.addItem(self.curveC)
            else:
                self.plot.removeItem(self.curveC)
                self.plot_ns.addItem(self.curveC)
            self.channelC_enable=True 
            self.channelC_disabled=False
            
    def graphics_channels_D(self):
        #Check the channel D
        mode_D=self.channel4.getMode()
        if not self.checkD.isChecked() and not self.channelD_disabled:
            if mode_D==2:
                self.plot.removeItem(self.curveD)
            else:
                self.plot_ns.removeItem(self.curveD)
                
            self.channelD_enable=False
            self.channelD_disabled=True
            
        if self.checkD.isChecked() and not self.channelD_enable:
            if mode_D==2:
                self.plot_ns.removeItem(self.curveD)
                self.plot.addItem(self.curveD)
            else:
                self.plot.removeItem(self.curveD)
                self.plot_ns.addItem(self.curveD)
            self.channelD_enable=True 
            self.channelD_disabled=False
    
    
    #To do: The function has many problems
    def new_start(self):
        pass
            # self.plot.removeItem(self.legend)
            # self.plot_ns.removeItem(self.legend_ns)
            # self.plot.removeItem(self.curve)
        
            # self.plot_ns.removeItem(self.curve)
        
        
            # self.plot.removeItem(self.curveB)
        
            # self.plot_ns.removeItem(self.curveB)
            
        
            # self.plot.removeItem(self.curveC)
        
            # self.plot_ns.removeItem(self.curveC)
        
        
            # self.plot.removeItem(self.curveD)
        
            # self.plot_ns.removeItem(self.curveD)
            # # self.curve=None
            # # self.curveB=None
            # # self.curveC=None
            # # self.curveD=None
            # # self.graphic_ms_ns()
            
    
    def graphic_ms_ns(self):
        #Extracting the mode of each channel
        mode_A=self.channel1.getMode()
        mode_B=self.channel2.getMode()
        mode_C=self.channel3.getMode()
        mode_D=self.channel4.getMode()

        
        #Histogram in the correct graph
        if mode_A==1:
            self.curve=self.plot_ns.plot(self.bins, self.hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150),name="ChannelA (Blue)")
        else:
            self.curve=self.plot.plot(self.bins, self.hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150),name="ChannelA (Blue)")
        
        if mode_B==1:
            self.curveB=self.plot_ns.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150),name="ChannelB (Red)")
        else:
            self.curveB=self.plot.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150),name="ChannelB (Red)")
        
        
        if mode_C==1:
            self.curveC=self.plot_ns.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150),name="ChannelC (Green)")
        else:
            self.curveC=self.plot.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150),name="ChannelC (Green)")
    
        if mode_D==1:
            self.curveD=self.plot_ns.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150),name="ChannelD (Yellow)")
        else:
            self.curveD=self.plot.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150),name="ChannelD (Yellow)")
            
    #Init
    def graphic_ms_ns_init(self):
        #Extracting the mode of each channel
        mode_A=self.channel1.getMode()
        mode_B=self.channel2.getMode()
        mode_C=self.channel3.getMode()
        mode_D=self.channel4.getMode()

        
        #Histogram in the correct graph
        if mode_A==1:
            self.curve=self.plot_ns.plot(self.bins, self.hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))
        else:
            self.curve=self.plot.plot(self.bins, self.hist, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))
        
        if mode_B==1:
            self.curveB=self.plot_ns.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150))
        else:
            self.curveB=self.plot.plot(self.binsB, self.histB, stepMode=True, fillLevel=0, brush=(255, 0, 0, 150))
        
        
        if mode_C==1:
            self.curveC=self.plot_ns.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150))
        else:
            self.curveC=self.plot.plot(self.binsC, self.histC, stepMode=True, fillLevel=0, brush=(0, 100, 0, 150))
    
        if mode_D==1:
            self.curveD=self.plot_ns.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150))
        else:
            self.curveD=self.plot.plot(self.binsD, self.histD, stepMode=True, fillLevel=0, brush=(220, 100, 0, 150))
            
    
    
    
    def update_plot(self):
    # We generate the data points to show the graphic
    # We verify the condition in order to get the graphics

        self.graphics_channels()
        self.graphics_channels_B()
        self.graphics_channels_C()
        self.graphics_channels_D()

        if self.sentinel:
            self.device.measure()

            new_data1 = self.get_new_data()  # Generar un valor y aleatorio entre 0 y 10
            new_data2 = self.get_new_data_B()  # Generar un valor y aleatorio entre 0 y 10
            new_data3 = self.get_new_data_C()  # Generar un valor y aleatorio entre 0 y 10
            new_data4 = self.get_new_data_D()  # Generar un valor y aleatorio entre 0 y 10

            #Agregar el nuevo punto de datos a las listas
            if new_data1 is not None:
                self.data.append(new_data1)
                self.update_histogram(self.data, self.curve, self.channel1)

            if new_data2 is not None:
                self.dataB.append(new_data2)
                self.update_histogram(self.dataB, self.curveB, self.channel2)

            if new_data3 is not None:
                self.dataC.append(new_data3)
                self.update_histogram(self.dataC, self.curveC, self.channel3)

            if new_data4 is not None:
                self.dataD.append(new_data4)
                self.update_histogram(self.dataD, self.curveD, self.channel4)
        
        #data=np.array(list(self.data)+list(self.dataB)+list(self.dataC)+list(self.dataD))   
        #self.maximum_visible(data)  

                
    def update_histogram(self, data, curve, channel):
        # Calcular el histograma
        hist, bins = np.histogram(data, bins=60)

        # Añadir un límite inferior a los bins para evitar barras muy delgadas
        curve.setData(bins, hist, stepMode="center", fillLevel=0, width=1.0)
        max_hist= max(hist)
        self.plot.setYRange(0,max_hist+2)
    
    
    def maximum_visible(self,data):
        # Obtener el rango de la vista actual
        x_range = self.plot.viewRange()[0]

        # Filtrar los datos que están dentro del rango visible del eje x
        visible_data = [value for value in data if x_range[0] <= value <= x_range[1]]

        if visible_data:
            # Recalcular el histograma solo para los datos visibles
            visible_hist, _ = np.histogram(visible_data, bins=60)

            # Obtener el valor máximo del histograma visible
            max_visible_value = max(visible_hist)

            # Ajustar el rango del eje y para que sea 2 unidades mayor que el valor máximo visible del histograma
            self.plot.setYRange(0, max_visible_value + 2)
        
        


                

    
    #Get data channel_A
    def get_new_data(self):
        
        number_runs=self.device.getNumberOfRuns()
        measurements=self.device.fetch()
        print(measurements)
        if len(measurements[0])!=0:
            total_measurement=0
            total_points=0
            for i in range(number_runs):
                if measurements[i][3]!=-1:
                    total_measurement+=measurements[i][3]
                    total_points+=1
            if total_points!=0:    
                average_measurement=total_measurement/total_points
                if self.channel1.getMode()==2:
                    miliseconds_measurement=average_measurement/(10**9)
                else:
                    miliseconds_measurement=average_measurement/(10**3)
                self.datapureA.append(round(average_measurement))
                return miliseconds_measurement
            else:
                return None
        else:
            return None
    
    #Get data channel_B
    def get_new_data_B(self):
        
        number_runs=self.device.getNumberOfRuns()
        measurements=self.device.fetch()
        
        if len(measurements[0])!=0:
            total_measurement=0
            total_points=0
            for i in range(number_runs):
                if measurements[i+number_runs][3]!=-1:
                    total_measurement+=measurements[i+number_runs][3]
                    total_points+=1
            if total_points!=0:    
                average_measurement=total_measurement/total_points
                if self.channel2.getMode()==2:
                    miliseconds_measurement=average_measurement/(10**9)
                else:
                    miliseconds_measurement=average_measurement/(10**3)
                self.datapureB.append(round(average_measurement))
                return miliseconds_measurement
            else:
                self.datapureB.append(8)
                return 4
        else:
            return None
    
    def get_new_data_C(self):
        
        number_runs=self.device.getNumberOfRuns()
        measurements=self.device.fetch()
        
        if len(measurements[0])!=0:
            total_measurement=0
            total_points=0
            for i in range(number_runs):
                if measurements[i+number_runs*2][3]!=-1:
                    total_measurement+=measurements[i+number_runs*2][3]
                    total_points+=1
            if total_points!=0:    
                average_measurement=total_measurement/total_points
                if self.channel3.getMode()==2:
                    miliseconds_measurement=average_measurement/(10**9)
                else:
                    miliseconds_measurement=average_measurement/(10**3)
                self.datapureC.append(round(average_measurement))
                return miliseconds_measurement
            else:
                self.datapureC.append(5)
                return 5
        else:
            return None
        
    def get_new_data_D(self):
        
        number_runs=self.device.getNumberOfRuns()
        measurements=self.device.fetch()
        
        if len(measurements[0])!=0:
            total_measurement=0
            total_points=0
            for i in range(number_runs):
                if measurements[i+number_runs*3][3]!=-1:
                    total_measurement+=measurements[i+number_runs*3][3]
                    total_points+=1
            if total_points!=0:    
                average_measurement=total_measurement/total_points
                
                if self.channel4.getMode()==2:
                    miliseconds_measurement=average_measurement/(10**9)
                else:
                    miliseconds_measurement=average_measurement/(10**3)
                self.datapureC.append(round(average_measurement))
                return miliseconds_measurement
            else:
                self.datapureD.append(1)
                return 1
        else:
            return None
    
    
    def zoom_changed(self):
        # Función llamada cuando cambia el rango de zoom en la gráfica
        x_range = self.viewbox.viewRange()[0] # Obtener el rango visible en el eje x
        
        x_min, x_max = x_range[0], x_range[1]
        
        bin_width = (x_max - x_min) / 100.0  # Ancho de cada bin para tener 100 bins en el rango visible
        self.bins = np.linspace(x_min, x_max, num=61)  # Crear 101 puntos para definir los bordes de los bins
        self.hist, _ = np.histogram(self.data, bins=self.bins)
        self.histB, _ = np.histogram(self.dataB, bins=self.bins)
        self.histC, _ = np.histogram(self.dataC, bins=self.bins)
        self.histD, _ = np.histogram(self.dataD, bins=self.bins)
        
        if self.channel1.getMode()==2:
            self.curve.setData(self.bins, self.hist)
        if self.channel2.getMode()==2:
            self.curveB.setData(self.bins, self.histB)
        if self.channel3.getMode()==2:    
            self.curveC.setData(self.bins, self.histC)
        if self.channel4.getMode()==2:    
            self.curveD.setData(self.bins, self.histD)
        data=np.array(list(self.data)+list(self.dataB)+list(self.dataC)+list(self.dataD))
        self.maximum_visible(data)
            
         # Obtener el rango actual del gráfico
        view_range = self.viewbox.viewRange()
        x_range = view_range[0]

        
        # Limitar el rango de zoom
        if x_range[1] - x_range[0] > 5:
            center_x = (x_range[1] + x_range[0]) / 2
            self.plot.setXRange(center_x - 5 / 2, center_x + 5 / 2)

        
    def zoom_changed2(self):
        # Función llamada cuando cambia el rango de zoom en la gráfica
        x_range = self.viewbox2.viewRange()[0]  # Obtener el rango visible en el eje x
        x_min, x_max = x_range[0], x_range[1]
        bin_width = (x_max - x_min) / 100.0  # Ancho de cada bin para tener 100 bins en el rango visible
        self.bins = np.linspace(x_min, x_max, num=61)  # Crear 101 puntos para definir los bordes de los bins
        self.hist, _ = np.histogram(self.data, bins=self.bins)
        self.histB, _ = np.histogram(self.dataB, bins=self.bins)
        self.histC, _ = np.histogram(self.dataC, bins=self.bins)
        self.histD, _ = np.histogram(self.dataD, bins=self.bins)
        if self.channel1.getMode()==1:
            self.curve.setData(self.bins, self.hist)
        if self.channel2.getMode()==1:
            self.curveB.setData(self.bins, self.histB)
        if self.channel3.getMode()==1:    
            self.curveC.setData(self.bins, self.histC)
        if self.channel4.getMode()==1:    
            self.curveD.setData(self.bins, self.histD)
            
        view_range = self.viewbox2.viewRange()
        x_range = view_range[0]

        # Limitar el rango de zoom
        if x_range[1] - x_range[0] > 500:
            center_x = (x_range[1] + x_range[0]) / 2
            self.plot_ns.setXRange(center_x - 500 / 2, center_x + 500 / 2)

    
    #To do delete the function
    def hide_graphic(self):
        self.win.close()
        self.verticalLayout.deleteLater()
    
    def hide_graphic2(self):
        self.startbutton.setEnabled(False)
        self.stopbutton.setEnabled(False)
        self.timer.stop()
    
    def show_graphic(self, device_new):
        self.device=device_new
        self.channel1=self.device.ch1
        self.channel2=self.device.ch2
        self.channel3=self.device.ch3
        self.channel4=self.device.ch4
        self.startbutton.setEnabled(True)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(3000)