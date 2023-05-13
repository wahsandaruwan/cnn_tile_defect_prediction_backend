# -----Imports-----
import cv2

# -----Camera initalization-----
camera = cv2.VideoCapture(0)

def gen_frames():
    """Generate frames continously from the webcam.
    """ 
    while True:
        # Read camera
        success, frame = camera.read()

        if not success:
            break
        else:
            # Encode image
            ret, buffers = cv2.imencode('.jpg', frame)
            new_frame = buffers.tobytes()
        
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + new_frame + b'\r\n')


