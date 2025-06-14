import os
import pathlib




#Create the folder
class createsavefile:
    def __init__(self):
        pass

    def create_folder_and_file(self):
        """
        Creates a folder named 'TempicoSoftwareData' inside the user's 'Documents' directory, 
        and creates a file named 'data_constants.txt' (or '.data_constants.txt' on Unix-based systems) inside that folder. 
        The file is populated with predefined default values for histogram and data names. 
        The file is hidden depending on the operating system.

        The folder and file are created with the following details:
        - Folder path: <Documents>/TempicoSoftwareData
        - File name: data_constants.txt (or '.data_constants.txt' for Unix-based systems)
        - The file contains the following default data:
        - Folder Path
        - Default Histogram Name
        - Default g2 Name
        - Default Lifetime Name

        In case of a Windows system, the file is made hidden using the Windows API. For Unix-based systems (Linux, macOS), 
        the file is renamed to be hidden by adding a dot ('.') before the filename.

        :raises OSError: If an error occurs during folder or file creation, or when accessing the filesystem.
        :returns: None
        """
        documents_dir = os.path.join(pathlib.Path.home(), "Documents")
        folder_name = "TempicoSoftwareData"
        folder_path = os.path.join(documents_dir, folder_name)
        file_name = "data_constants.txt"
        file_path = os.path.join(folder_path, file_name)

        try:
            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, "w") as file:
                file.write(f"Folder Path: {folder_path}\n")
                file.write(f"Default Histogram Name: histogram_data\n")
                file.write(f"Default g2 Name: g2_data\n")
                file.write(f"Default Lifetime Name: lifetime_data\n")
            
            # Ocultar el archivo de manera efectiva según el sistema operativo
            if os.name == 'nt':  # Windows
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
                print(f"The folder '{folder_name}' and the hidden file '{file_name}' have been created in '{documents_dir}'.")
            else:  # Unix-based (Linux, macOS)
                hidden_file_path = os.path.join(folder_path, f".{file_name}")
                os.rename(file_path, hidden_file_path)
                print(f"The folder '{folder_name}' and the hidden file '.{file_name}' have been created in '{documents_dir}'.")

        except OSError as e:
            print(f"Error occurred while creating the folder and/or file: {e}")
            

    #Check if the folder already exist 

    def check_folder_and_file(self):
        """
        Checks whether the folder 'TempicoSoftwareData' and the file 'data_constants.txt' 
        exist in the user's 'Documents' directory.

        The function constructs the paths for both the folder and the file, and checks if both exist:
        - Folder path: <Documents>/TempicoSoftwareData
        - File name: data_constants.txt

        If both the folder and the file exist, the function returns True. Otherwise, it returns False.

        :returns: bool: True if the folder and file exist, False otherwise.
        """
        documents_dir = os.path.join(pathlib.Path.home(), "Documents")
        folder_name = "TempicoSoftwareData"
        file_name = "data_constants.txt"
        folder_path = os.path.join(documents_dir, folder_name)
        file_path = os.path.join(folder_path, file_name)
        valor=False

        if os.path.exists(folder_path) and os.path.exists(file_path):
            valor= True
        
        return valor

    #Create the folder

    def create_folder(self):
        """
        Checks if the specified folder and file already exist. If they do exist, it creates 
        the folder and file by calling the 'create_folder_and_file' function.

        :returns: None
        """
        value=self.check_folder_and_file()
        if value:
            self.create_folder_and_file()
            
    #Get the dictionary with the constants
        
    def read_default_data(self):
        """
        Reads the default data from the file 'data_constants.txt' located in the 
        'TempicoSoftwareData' folder inside the user's 'Documents' directory.

        This function attempts to read the file line by line and extracts key-value pairs 
        formatted as "key: value". The first line, which contains the folder path, is 
        processed separately. The extracted key-value pairs are stored in a dictionary, 
        which is returned as the output.

        If the file is not found or an error occurs while reading the file, the function
        returns None.

        :returns: dict or None: A dictionary containing the data from the file, or None if 
                an error occurred.
        """
        # Get the path to the "Documents" directory on the current operating system
        documents_dir = os.path.join(pathlib.Path.home(), "Documents")

        # Specify the folder name and file name
        folder_name = "TempicoSoftwareData"
        if os.name == 'posix':  
            file_name = ".data_constants.txt"
        else:  
            file_name = "data_constants.txt"

        # Construct the full path to the file
        file_path = os.path.join(documents_dir, folder_name, file_name)

        try:
            data_dict = {}

            # Open the file in read mode
            with open(file_path, "r") as file:
                # Read each line of the file
                number=0
                for line in file:
                    # Split the line into key and value (assuming it's in the format "key: value")
                    if number==0:
                        key,value= 'Folder path',line.split(': ')[1].replace('\n','')
                        data_dict[key]=value
                        number=1
                    key_value = line.strip().split(":")
                    if len(key_value) == 2:
                        key, value = key_value[0].strip(), key_value[1].strip()
                        data_dict[key] = value
            file.close()

            return data_dict

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
            return None
        except Exception as e:
            print(f"Error while reading the file '{file_path}': {e}")
            return None

    #Save the files in a txt files in the folder created
    def save_lists_as_columns_txt(self,data_lists, file_names, column_names, path,settings, extension):
        """
        Saves multiple lists of data as separate text files, where each list is written as a 
        column in the text file. The files are saved in the specified directory with the 
        provided file names, and the columns are named based on the given column names. 

        This function ensures that the specified directory exists, and raises an error if 
        the lengths of the input lists do not match.

        :param data_lists: A list of lists, where each list contains the data to be written to a file (list).
        :param file_names: A list of strings specifying the names of the output files (list of str).
        :param column_names: A list of strings specifying the names of the columns in the text files (list of str).
        :param path: The directory path where the files will be saved (str).
        :param settings: A list of settings to be written as the first line in each file (list of str).
        :param extension: The file extension for the output files (str).
        :raises ValueError: If the lengths of data_lists, file_names, and column_names do not match.
        :returns: None
        """
        if not os.path.exists(path):
            os.makedirs(path)
            
        if len(data_lists) != len(file_names) or len(data_lists) != len(column_names):
            raise ValueError("Data lists, file names, and column names must have the same length.")
            
        for file_name, data_list, column_name,setting_channel in zip(file_names, data_lists, column_names,settings):
            full_file_path = os.path.join(path, f"{file_name}."+str(extension))
            
            with open(full_file_path, 'w') as file:
                file.write(f"{setting_channel}\n")
                file.write(f"{column_name}\n")
                for element in data_list:
                    file.write(f"{element}\n")
                file.close()
                
    def save_g2_data(self,data, file_name, folder_path, settings, extension, textLabel):
        """
        Saves g2 data (tau and g2 values) into a text file in a specified folder. The function
        ensures that the provided tau and g2 values have the same length and writes them into 
        a file along with specified settings and a label for the g2 values.

        The file is saved in the specified folder path, with the provided file name and extension.

        :param data: A tuple where the first element is a list of tau values and the second 
                    element is a list of corresponding g2 values (tuple of lists).
        :param file_name: The name of the output file (str).
        :param folder_path: The path to the folder where the file will be saved (str).
        :param settings: A string representing the settings to be written in the first line of the file (str).
        :param extension: The file extension for the output file (str).
        :param textLabel: A label to be written before the g2 values in the file (str).
        :raises ValueError: If the lengths of the tau and g2 value lists do not match.
        :returns: None
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if len(data[0]) != len(data[1]):
            raise ValueError("Tau and g2 Values must have the same length")
        else:
        
            full_path = os.path.join(folder_path, f"{file_name}.{extension}")
            
            with open(full_path, 'w') as file:
                file.write(settings + '\n')
                
                file.write(textLabel+"\tg2 Values\n")
                
                for tau, g2_value in zip(data[0], data[1]):
                    file.write(f"{tau}\t{g2_value}\n")
                    
    def save_LifeTime_data(self,data, file_name, folder_path, settings, extension, textLabel):
        """
        Saves LifeTime data (time and LifeTime values) into a text file in a specified folder. The function
        ensures that the provided time and LifeTime values have the same length and writes them into 
        a file along with specified settings and a label for the LifeTime values.

        The file is saved in the specified folder path, with the provided file name and extension.

        :param data: A tuple where the first element is a list of time values and the second 
                    element is a list of corresponding LifeTime values (tuple of lists).
        :param file_name: The name of the output file (str).
        :param folder_path: The path to the folder where the file will be saved (str).
        :param settings: A string representing the settings to be written in the first line of the file (str).
        :param extension: The file extension for the output file (str).
        :param textLabel: A label to be written before the LifeTime values in the file (str).
        :raises ValueError: If the lengths of the time and LifeTime value lists do not match.
        :returns: None
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if len(data[0]) != len(data[1]):
            raise ValueError("Time and LifeTime Values must have the same length")
        else:
        
            full_path = os.path.join(folder_path, f"{file_name}.{extension}")
            
            with open(full_path, 'w') as file:
                file.write(settings + '\n')
                
                file.write(textLabel+"\tCounts LifeTime\n")
                
                for tau, LifeTimeValue in zip(data[0], data[1]):
                    file.write(f"{tau}\t{LifeTimeValue}\n")
    def save_counts_data(self,time_stamp,data,dataUncertainties,filenames,folder_path,settings, extension,channels):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if len(time_stamp)!= len(data):
            raise ValueError("Time stamps and measurement must have the same lenght")
        else:
            for file_name,timeStamp, data_list,data_uncertainties,setting_channel, channel in zip(filenames,time_stamp, data,dataUncertainties,settings,channels):
                full_path=os.path.join(folder_path, f"{file_name}.{extension}")
                
                with open(full_path, 'w') as file:
                    file.write(setting_channel + '\n')
                    file.write(f"Hour (HH:MM:SS) \t Counts Channel {channel}(counts/sec) \t Uncertainties Channel {channel}(counts/sec)\n")
                    for timeStamp, countValue,uncertanty in zip(timeStamp,data_list,data_uncertainties):
                        valueFormated= f"{countValue:.5f}"
                        uncertaintyFormated=f"{uncertanty:.5f}"
                        file.write(f"{timeStamp}\t{valueFormated}\t\t{uncertaintyFormated}\n")

    
    

