import hid
import serial.tools.list_ports
import serial

class PyTempicoManager:
    """
    Class for managing the search and connection of Tempico devices connected to serial ports on the PC.

    This class is responsible for scanning the available serial ports on the system and searching for Tempico devices 
    connected to those ports. It facilitates interaction with Tempico devices by allowing their identification and connection.

    :param None: No parameters are required for the initialization of the class.
    :return: None
    """
    def __init__(self):
        pass
    
    # Function to get the vid and pid in two variables
    def get_vid_pid(self, vid_pid_information):
        """
        Extracts the Vendor ID (VID) and Product ID (PID) from a string and returns them as a tuple.

        This function processes a string that contains the VID and PID information in the format 
        'VID:PID=xxxx:yyyy'. It splits the string and retrieves the VID and PID values, returning 
        them as a tuple of strings.

        :param vid_pid_information: A string containing the VID and PID information.
        :type vid_pid_information: str
        :returns: A tuple containing the VID and PID as strings (vid, pid).
        :rtype: tuple
        """
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

    # Verify if the vid and pid corresponds to a Tempico
    def verify_pyTempico(self, tuple_vid_pid):
        """
        Verifies whether the connected device is a Tempico device.

        This function checks if the device’s Vendor ID (VID) and Product ID (PID) match the values 
        corresponding to a Tempico device. It returns `True` if the device is identified as a Tempico, 
        and `False` otherwise.

        :param tuple_vid_pid: A tuple containing the VID and PID of the device.
        :type tuple_vid_pid: tuple
        :returns: `True` if the device is a Tempico, `False` otherwise.
        :rtype: bool
        """
        vid = tuple_vid_pid[0]
        pid = tuple_vid_pid[1]
        if vid == "04D8" and pid == "00DD":
            value = self.find_devices(vid, pid)
        else:
            value = self.find_devices(vid, pid)
        return value

    # Function to open and get the manufacturer
    def find_devices(self, vid_s, pid_s):
        """
        Finds and verifies whether a device with the given VID and PID is a Tempico device.

        This function takes the Vendor ID (VID) and Product ID (PID) as inputs, converts them to integers, 
        and attempts to open the device using these values. It then checks if the manufacturer and product 
        strings match the expected values for a Tempico device.

        :param vid_s: The Vendor ID (VID) of the device in string format.
        :type vid_s: str
        :param pid_s: The Product ID (PID) of the device in string format.
        :type pid_s: str
        :returns: `True` if the device is a Tempico, `False` otherwise.
        :rtype: bool
        """
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
        """
        Searches for Tempico devices among the available serial ports and returns a list of their port names.

        This function scans the system's serial ports, checks if they correspond to a Tempico device by
        retrieving the VID and PID, and verifies if they match the Tempico device specifications.
        Bluetooth devices are excluded from the search.

        :returns: A list of port names corresponding to Tempico devices.
        :rtype: list of str
        """
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

