import os
import pathlib




#Create the folder

def create_folder_and_file():
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
            file.close()
        
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

def check_folder_and_file():
    
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

def create_folder():
    value=check_folder_and_file()
    if value:
        create_folder_and_file()
        
#Get the dictionary with the constants
    
def read_default_data():
    # Get the path to the "Documents" directory on the current operating system
    documents_dir = os.path.join(pathlib.Path.home(), "Documents")

    # Specify the folder name and file name
    folder_name = "TempicoSoftwareData"
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
def save_lists_as_columns_txt(data_lists, file_names, column_names, path,settings, extension):
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

create_folder_and_file()