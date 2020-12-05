from flask import Flask, render_template, Response
from monitor_package import app
import cv2


# camera = cv2.VideoCapture('rtsp://username:password@ip_address:554/user=username_password=password'_channel=channel_number_stream=0.sdp')
camera = cv2.VideoCapture("rtsp://admin:admin@192.168.0.104:554/user=username_password=password'_channel=channel_number_stream=0.sdp")

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template("index.html")