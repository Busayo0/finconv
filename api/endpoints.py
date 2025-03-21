## api/endpoints.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from utils.auto_detect import AutoFileConverter
from converters.csv_converter import CSVTransactionConverter
from converters.json_converter import JSONTransactionConverter
from converters.xml_converter import XMLTransactionConverter
from converters.iso8583_converter import ISO8583TransactionConverter

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    processor: str = Form("Visa"),
    output_format: str = Form("csv")
):
    file_id = uuid.uuid4().hex
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detector = AutoFileConverter()
    file_type = detector.detect_format(input_path)

    if file_type == "csv":
        converter = CSVTransactionConverter(processor)
    elif file_type == "json":
        converter = JSONTransactionConverter(processor)
    elif file_type == "xml":
        converter = XMLTransactionConverter()
    elif file_type == "iso8583":
        converter = ISO8583TransactionConverter()
    else:
        return {"error": "Unsupported file format."}

    output_file = input_path.replace(os.path.splitext(input_path)[1], f"_converted.{output_format}")
    converter.convert(input_path, output_format)

    return FileResponse(path=output_file, filename=os.path.basename(output_file), media_type="application/octet-stream")
