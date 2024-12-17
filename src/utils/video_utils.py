import cv2
import base64

def encode_frame_to_base64(frame):
    """Convert OpenCV frame to base64 string"""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def resize_frame(frame, width, height):
    """Resize frame to specified dimensions"""
    return cv2.resize(frame, (width, height))