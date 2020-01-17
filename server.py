import io
import tornado.web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.websocket import WebSocketHandler
from picamera import PiCamera

class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello, World')

class WebSocket(tornado.websocket.WebSocketHandler):
       
    def open(self):
        print("[WS]: opened")
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (300, 300)
        self.camera.framerate = 15

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
        self.camera.capture(sio, "jpeg", use_video_port=True)

        try:
            self.write_message(sio.getvalue(), binary=True)
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()
    
handlers = [
    (r"/", WebSocket),
    (r"/status", StatusHandler)
]

app = tornado.web.Application(handlers)
app.listen(8080)
print('[Server]: Running ...')
IOLoop.current().start()
