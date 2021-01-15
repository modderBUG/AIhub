from werkzeug.utils import secure_filename
from loguru import logger
from PIL import Image
from io import BytesIO
import base64


def img_to_base64(upload_files):
    for file in upload_files:
        filename = secure_filename(file.filename)
        logger.info(filename)
    img1 = Image.open(upload_files[0])
    img_buffer = BytesIO()
    img1.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    img = base64.b64encode(byte_data)
    return img
