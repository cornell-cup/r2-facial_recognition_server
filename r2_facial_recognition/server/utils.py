import io
from PIL import Image
import numpy as np
import cv2


def img_from_bytes(bytes_: bytes) -> np.ndarray:
    img_io = io.BytesIO(bytes_)
    # np.asarray(Image.open(img_io)) yields the correct result, but am
    #  unsure if it is the correct way to write it.
    return cv2.cvtColor(np.asarray(Image.open(img_io)), cv2.COLOR_RGB2BGR)
