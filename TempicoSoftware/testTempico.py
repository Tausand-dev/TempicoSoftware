#PyTemmpico Examples
#This is a script only using Pytempico functions

#Import the library
import pyTempico
#Get the information of Tempico device
def specs_function():
    My_tempico_device=pyTempico.TempicoDevice('COM12')
    #Open the connection between the object and hardware
    My_tempico_device.open()
    print("Id: "+str(My_tempico_device.id_tempico_device))
    print("Retruns if there is a connection open: "+str(My_tempico_device.isOpen()))
    print("The baudrate of the serial is "+str(My_tempico_device.device.baudrate))
    print("The number of channels are "+str(My_tempico_device.number_of_channels))
    print("The number of runs are "+str(My_tempico_device.number_of_runs))
    print("The serial port "+str(My_tempico_device.port))
    print("The threshold voltage is "+str(My_tempico_device.threshold))
    print("The firmware version is "+str(My_tempico_device.getFirmware()))
    print("The identification is "+str(My_tempico_device.getIdn()))
    print("The settings are "+str(My_tempico_device.getSettings()))
    print("The threshold voltage is (again): "+str(My_tempico_device.getThresholdVoltage()))
    print("Returns if is a pending message is available: "+str(My_tempico_device.isPendingReadMessage()))
    #Close the connection between the object and hardware
    My_tempico_device.close()

def specs_function_ch2():
    My_tempico_device=pyTempico.TempicoDevice('COM12')
    #Open the connection between the object and hardware
    My_tempico_device.open()
    #Get the ch2
    channel2=My_tempico_device.ch2
    print("The id of the channel is:"+str(channel2.id_tempico_channel))
    print("The id of the tempico devic linked to the ch2 is:"+str(channel2.id_tempico_device))
    print("The number of the channel is:"+str(channel2.channel_number))
    print("Return if the channel is enable:"+str(channel2.enable))
    print("The mode of the channel:"+str(channel2.mode))
    print("The number of the stops is :"+str(channel2.number_of_stops))
    print("The start edge is :"+str(channel2.start_edge))
    print("The stop edge is :"+str(channel2.stop_edge))
    print("The stop mask is: "+str(channel2.stop_mask) )
    print("The average cycles are: "+str(channel2.getAverageCycles()))
    
    #Close the connection between the object and hardware
    My_tempico_device.close()


#Measurement1
def create_measurement_ch2_1():
    My_tempico_device=pyTempico.TempicoDevice('COM12')
    #Open the connection between the object and hardware
    My_tempico_device.open()
    #Get the ch2
    channel2=My_tempico_device.ch2
    channel2.setMode(2)
    My_tempico_device.setNumberOfRuns(2)
    #Measurement
    My_tempico_device.measure()
    channel2.setNumberOfStops(1)
    print("The measurement of tempico device is: "+str(My_tempico_device.fetch()))
    #Close the connection between the object and hardware
    My_tempico_device.close()  




#Measurement2
def create_measurement_ch2_2():
    My_tempico_device=pyTempico.TempicoDevice('COM12')
    #Open the connection between the object and hardware
    My_tempico_device.open()
    #Get the ch2
    channel2=My_tempico_device.ch2
    channel2.setMode(2)
    My_tempico_device.setNumberOfRuns(4)
    #Measurement
    My_tempico_device.measure()
    channel2.setNumberOfStops(3)
    print("The measurement of tempico device is: "+str(My_tempico_device.fetch()))
    #Close the connection between the object and hardware
    My_tempico_device.close()    

#Measurement3
def create_void_measurement_ch2():
    My_tempico_device=pyTempico.TempicoDevice('COM12')
    #Open the connection between the object and hardware
    My_tempico_device.open()
    #Get the ch2
    channel2=My_tempico_device.ch3
    channel2.setMode(2)
    channel2.setStartEdge('FALL')
    channel2.setStopEdge('FALL')
    My_tempico_device.setNumberOfRuns(1)
    #Measurement
    My_tempico_device.measure()
    channel2.setNumberOfStops(1)
    channel2.setStartEdge('RISE')
    channel2.setStopEdge('RISE')
    #channel2.enableChannel()
    print("The measurement of tempico device is: "+str(My_tempico_device.fetch()))
    #Close the connection between the object and hardware
    My_tempico_device.close()    





def show_menu():
    print("""
    Options:
    1. Example of Information about the device and settings
    2. Example of Information about Ch2 and settings
    3. Example of measurement 1
    4. Example of measurement 2
    5. Example of void measurement 
          
    6. Exit
    """)




def Menu():
    while True:
        show_menu()
        opcion = input("Write an option: ")      
        if opcion == '1':
            specs_function()
        elif opcion == '2':
            specs_function_ch2()
        elif opcion == '3':
            create_measurement_ch2_1()
        elif opcion == '4':
            create_measurement_ch2_2()
        elif opcion == '5':
            create_void_measurement_ch2()
        elif opcion == '6':
            print("Saliendo del menú...")
            break
        else:
            print("Invalid Option. Please Try Again")
if __name__ == "__main__":
    Menu()