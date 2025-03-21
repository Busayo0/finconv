## utils/auto_detect.py
import magic

class AutoFileConverter:
    def detect_format(self, file_path):
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)

        if "csv" in file_type:
            return "csv"
        elif "json" in file_type:
            return "json"
        elif "xml" in file_type:
            return "xml"
        elif "octet-stream" in file_type or file_path.endswith(".dat"):
            return "iso8583"
        else:
            raise ValueError("Unsupported file format")
