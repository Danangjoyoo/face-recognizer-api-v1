from fastapi import UploadFile
import numpy as np
import cv2


async def read_image(file: UploadFile):
    img_str = await file.read()
    nparr = np.fromstring(img_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np