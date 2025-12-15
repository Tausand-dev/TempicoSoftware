from PySide2.QtCore import QThread, Signal

class ProcessingDataSaved(QThread):
    """
    Thread class responsible for processing saved measurement files when autosave is not enabled.

    This class runs in a separate thread to avoid blocking the main UI while
    processing data from a previously saved file. It emits progress updates so
    the user interface can reflect the current status of the processing task.

    Main responsibilities:
    - Read and process the specified saved data file.
    - Emit progress updates during the processing.
    - Operate independently from the main thread to keep the UI responsive.

    Signals:
        changeProgress (float):
            Emitted to update the processing progress in the UI as a percentage.

    :param filename: Path to the saved measurement file to be processed.
    """
    changeProgress=Signal(float)
    def __init__(self, filename):
        super().__init__()
        self.filename=filename
    
    def run(self):
        self.sortTimeStamps(self.filename)
    
    def sortTimeStamps(self, file_path):
        """
        Sorts a saved timestamp file by start times and emits progress updates during processing.

        This function reads the specified measurement file, parses its data entries,
        sorts them chronologically by start time, and writes the sorted content back
        to the same file. Progress updates are emitted throughout the process to
        inform the UI of the current completion percentage.

        :param file_path: Path to the saved measurement file to be sorted.
        :return: None
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            self.changeProgress.emit(100)
            return

        header = lines[:8]
        data_lines = lines[7:]
        total_lines = len(data_lines)
        parsed_data = []
        selectedFormat=file_path.split(".")[-1]
        if selectedFormat=="csv":
            separator=";"
        else:
            separator="\t"

        for idx, line in enumerate(data_lines):
            parts = line.strip().split(separator)
            if len(parts) == 3:
                start_time_str, stop_time, channel = parts
                try:
                    parsed_data.append((start_time_str, stop_time, channel))
                except ValueError:
                    continue

            if idx % max(1, total_lines // 30) == 0:
                percent = int((idx + 1) / total_lines * 30)
                self.changeProgress.emit(percent)

        self.changeProgress.emit(70)

        sorted_data = sorted(parsed_data, key=lambda x: x[0])

        self.changeProgress.emit(70)  

        with open(file_path, 'w', encoding='utf-8') as file:
            for headerValue in header:
                file.write(headerValue)
            for idx, (start_time, stop_time, channel) in enumerate(sorted_data):
                file.write(f"{start_time}{separator}{stop_time}{separator}{channel}\n")

                if idx % max(1, len(sorted_data) // 30) == 0:
                    percent = 70 + int((idx + 1) / len(sorted_data) * 30)
                    self.changeProgress.emit(percent)

        self.changeProgress.emit(100)