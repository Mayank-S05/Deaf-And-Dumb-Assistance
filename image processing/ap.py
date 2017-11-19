from flask import Flask, render_template, Response
from camera import VideoCamera
# from flask_socketio import SocketIO, emit


app = Flask(__name__)
var='no'
string = "q"
count = 0
# app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
# socketio = SocketIO( app )

@app.route('/')
def index():
    return render_template('index.html',var=var)

def gen(camera):
    tf = camera.get_tf()
    with tf.Session() as sess:
    	while True:
        	frame,var = camera.get_frame(sess)
        	yield (b'--frame\r\n'
             		b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        	print(var)
        	# if(var != 'no'):
        	# 	if(var == 'a' or var == 'b' or var == 'c' or var == 'd'):
		       #      print(var , end='')
		       #  elif(var == 'space'):
		       #      print(' ', end='')
		       #  else:
		       #      print('',end='')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	# socketio.run( app, debug = True )
	app.run(host='127.0.0.1', debug=True, port=5000)
