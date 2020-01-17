import io
import tornado.web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.websocket import WebSocketHandler
from picamera import PiCamera

camera = PiCamera()
camera.rotation = 180
camera.resolution = (300, 300)
camera.framerate = 15

class WebSocket(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print("[WS]: opened")
        self.camera_loop = PeriodicCallback(self.loop, 500)
        self.camera_loop.start()

    def on_message(self, message):
        print(f'[WS]: received message: {message}')

    def on_close(self):
        print("[WS]: closed")

    def check_origin(self, origin):
        return True

    def loop(self):
        sio = io.BytesIO()
        camera.capture(sio, "jpeg", use_video_port=True)

        try:
            self.write_message(sio.getvalue(), binary=True)
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()
    
handlers = [(r"/", WebSocket)]
app = tornado.web.Application(handlers)
app.listen(8080)
print('[Server]: Running ...')
IOLoop.current().start()
