"""sensor_msgs/Image <-> numpy helpers (no cv_bridge needed)."""
import numpy as np
from sensor_msgs.msg import Image

# encoding -> (channels, channel order to reach BGR)
_ENCODINGS = {
    "bgr8": (3, None),
    "rgb8": (3, [2, 1, 0]),
    "bgra8": (4, [0, 1, 2]),
    "rgba8": (4, [2, 1, 0]),
    "mono8": (1, None),
}


def image_to_bgr(msg: Image) -> np.ndarray:
    """sensor_msgs/Image -> HxWx3 uint8 BGR array."""
    if msg.encoding not in _ENCODINGS:
        raise ValueError(f"unsupported encoding '{msg.encoding}'")
    ch, order = _ENCODINGS[msg.encoding]
    buf = np.frombuffer(msg.data, dtype=np.uint8)
    img = buf.reshape(msg.height, msg.step)[:, : msg.width * ch].reshape(msg.height, msg.width, ch)
    if ch == 1:
        return np.repeat(img, 3, axis=2)
    return np.ascontiguousarray(img[:, :, order] if order else img)


def bgr_to_image(img: np.ndarray, header) -> Image:
    msg = Image()
    msg.header = header
    msg.height, msg.width = img.shape[:2]
    msg.encoding = "bgr8"
    msg.step = msg.width * 3
    msg.data = np.ascontiguousarray(img).tobytes()
    return msg


def rotate_cw(img: np.ndarray, degrees: int) -> np.ndarray:
    """Rotate clockwise by 0/90/180/270 degrees.

    Dumm-E's wrist camera is mounted on its side, so its raw frames need 90 deg
    clockwise to be upright (people standing up, bed at the bottom).
    """
    degrees %= 360
    if degrees not in (0, 90, 180, 270):
        raise ValueError("image_rotation must be 0, 90, 180 or 270")
    return np.ascontiguousarray(np.rot90(img, k=-degrees // 90)) if degrees else img
