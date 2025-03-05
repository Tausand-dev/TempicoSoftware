import hid
import serial.tools.list_ports
import serial

class PyTempicoManager:
    def __init__(self):
        pass
    
    # Function to get the vid and pid in two variables
    def get_vid_pid(self, vid_pid_information):
        without_spaces = vid_pid_information.split(' ')
        tuple = ()
        key_word = 'VID:PID'
        for i in without_spaces:
            if key_word in i:
                vid_pid_value = i.split('=')
                numbers_value = vid_pid_value[1].split(":")
                vid = numbers_value[0]
                pid = numbers_value[1]
                tuple = (vid, pid)
        return tuple

    # Verify if the vid and pid corresponds to a pytempico
    def verify_pyTempico(self, tuple_vid_pid):
        vid = tuple_vid_pid[0]
        pid = tuple_vid_pid[1]
        if vid == "04D8" and pid == "00DD":
            value = self.find_devices(vid, pid)
        else:
            value = self.find_devices(vid, pid)
        return value

    # Function to open and get the manufacturer
    def find_devices(self, vid_s, pid_s):
        vid = int(vid_s, 16)
        pid = int(pid_s, 16)

        try:
            h = hid.device()
            h.open(vid, pid)
            Manufacturer = h.get_manufacturer_string()
            Product = h.get_product_string()
            if Manufacturer == "Tausand electronics" and "Tempico" in Product:
                h.close()
                return True
            else:
                h.close()
                return False
        except:
            return False

    # Function to get the list of ports with a pytempico devices
    def get_pytempico_devices(self):
        ports = []
        puertos = serial.tools.list_ports.comports()
        if not puertos:
            print("No serial ports found.")
        else:
            bluetooth_word = "Bluetooth"
            for puerto in puertos:
                description = puerto.description
                if bluetooth_word not in description:
                    vid_pid_string = puerto.hwid
                    values_packet = self.get_vid_pid(vid_pid_string)
                    if len(values_packet) == 2:
                        value = self.verify_pyTempico(values_packet)
                        if value == True:
                            ports.append(puerto.name)
                if "Tempico" in description:
                    ports.append(puerto.device)
        return ports

