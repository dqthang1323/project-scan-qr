from flask import Flask, render_template, Response
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import webbrowser
app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            encoding = 'utf-8'
            
            _,frame1 = camera.read()
            barcodes = pyzbar.decode(frame1)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                url = str(barcodes[0].data, encoding=encoding)
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                print (text)
                cv2.putText(frame1, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if barcodeType == 'EAN13':

                    webbrowser.open("https://www.barcodelookup.com/"+barcodeData)
                    time.sleep(2)
                elif barcodeType == "QRCODE":
                    webbrowser.open(url)
                    time.sleep(2)
  

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)