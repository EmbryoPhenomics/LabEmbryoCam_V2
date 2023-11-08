import cv2
from tqdm import tqdm
import time as timelib
from collections import deque
import threading
from more_itertools import pairwise
import numpy as np
import matplotlib.pyplot as plt

from camera_benchmark import CaptureBenchmark

feature_flags = {
    "framerate": cv2.CAP_PROP_FPS,
    "exposure": cv2.CAP_PROP_EXPOSURE,
    "contrast": cv2.CAP_PROP_CONTRAST,
    "width": cv2.CAP_PROP_FRAME_WIDTH,
    "height": cv2.CAP_PROP_FRAME_HEIGHT,
}

class CaptureGenerator:
    def __init__(self, cam_cls):
        self.cam_cls = cam_cls
        self.cam_cls.camera.release()
        self.cam_cls.camera = cv2.VideoCapture(self.cam_cls.port)
        self.shutdown = threading.Event()
        self.cam_cls.benchmarker.clear()

    def __enter__(self):
        print('Start.')
        self.cam_cls.benchmarker.record_start()

        while True:
            if self.shutdown.is_set():
                break
            else:
                ret, frame = self.cam_cls.camera.read()
                self.cam_cls.benchmarker.record_frame_time()

                if not ret:
                    self.cam_cls.benchmarker.record_incomplete()
                else:
                    self.cam_cls.benchmarker.record_complete()
                    yield frame
                    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print('Finished.')
        self.cam_cls.benchmarker.record_end()
        self.cam_cls.camera.release()

        if self.cam_cls.benchmark:
            self.cam_cls.benchmarker.print_log()

class OpenCV_Pi:
    def __init__(self, port=0, benchmark=True):
        self.port = port
        self.benchmark = benchmark 
        self.benchmarker = CaptureBenchmark()

        try:
            self.camera = cv2.VideoCapture(port)
        except:
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def close(self):
        self.camera.release()

    def get(self, name):
        return self.camera.get(feature_flags[name])

    def set(self, name, value):
        self.camera.set(feature_flags[name], value)

    def grab(self):
        self.camera.release()
        self.camera = cv2.VideoCapture(self.port)
        ret, frame = self.camera.read()
        self.camera.release()
        return frame

    def _capture_callback(self, callback):
        self.camera.release()
        self.camera = cv2.VideoCapture(self.port)
        self.shutdown = threading.Event()
        self.benchmarker.clear()
        self.benchmarker.record_start()

        while True:
            if self.shutdown.is_set():
                break
            else:
                ret, frame = self.camera.read()
                self.benchmarker.record_frame_time()

                if not ret:
                    self.benchmarker.record_incomplete()
                else:
                    callback(frame)
                    self.benchmarker.record_complete()

        self.benchmarker.record_end()
        self.camera.release()

        if self.benchmark:
            self.benchmarker.print_log()

    def start_capture_stream(self, callback=None):
        if callback is not None:
            self._capture_callback(callback)
        else:
            return CaptureGenerator(self)

    def _display(self, frame):
        key = cv2.waitKey(1)
        if key == 27:
            self.shutdown.set()
            cv2.destroyAllWindows()
        else:
            cv2.imshow('Live Stream', frame)   

    def stream(self):
        self.start_capture_stream(self._display)

    def frame_to_bytes(self, frame):
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()        

    def _read(self, frame):
        if self.counter == 0:
            self.end_time = timelib.time() + self.acq_time

        current = timelib.time()
        if current <= self.end_time:
            self.frame_queue.append(frame)
            self.counter += 1

        elif current > self.end_time:
            self.frame_queue.append(None)
            self.shutdown.set()
            
    def _write(self, frame_queue):
        while True:
            if len(frame_queue):
                frame = frame_queue.popleft()

                if frame is None:
                    break
                else:
                    self.writer.write(frame)
                    self.pgbar.update(1)

    def acquire(self, path, time):
        self.counter = 0
        self.acq_time = time

        # Start up frame consumer
        fps = int(self.get('framerate'))
        h, w, _ = self.grab().shape
        self.writer = cv2.VideoWriter(path, 0, fps, (w, h))

        self.frame_queue = deque()
        consume_thread = threading.Thread(target=self._write, args=(self.frame_queue,))
        consume_thread.start()

        print('Acquisition progress:')
        self.pgbar = tqdm(total=round(fps*time))

        # Start frame producer
        self.start_capture_stream(self._read)

        self.writer.release()
        self.pgbar.close()

if __name__ == '__main__':
    camera = OpenCV_Pi()
    for frame in camera.start_capture_stream(camera._display):
        print(frame.shape)


