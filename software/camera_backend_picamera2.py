import cv2
import picamera2
from tqdm import tqdm
import time

import cv2 
import time as timelib
from tqdm import tqdm
from collections import deque
import numpy as np
import threading
import re
import pandas as pd
import subprocess as sp
import atexit
import gc
import re
import math
import vuba
from tkinter import *
from PIL import ImageTk

from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput, FfmpegOutput
import simplejpeg

from camera_benchmark import CaptureBenchmark

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (255,255,255)
lineType = 1

class LiveOptFlow:
    '''
    Real-time optical flow visualisation

    This is a real-time application for sparse optical flow, operating on the live
    stream produced by the camera instance. 

    Parameters for sparse optical flow are hardcoded in __init__ below but you
    may need to change these depending on your application.

    '''
    def __init__(self):
        self.feature_params = dict(
            maxCorners=500,
            qualityLevel=0.001,
            minDistance=0,
            blockSize=7,
            useHarrisDetector=0,
            k=0.4,
        )

        # Parameters for lucas kanade optical flow
        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
        )

    def register_first(self, frame):
        self.first = frame
        self.p0 = cv2.goodFeaturesToTrack(frame, mask=None, **self.feature_params)
        self.rot_mask = cv2.cvtColor(np.zeros_like(frame), cv2.COLOR_GRAY2BGR)
        self.point_log = deque(maxlen=5) # Max point memory of 5

    def render(self, frame):
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.first, frame, self.p0, None, **self.lk_params)
    
        frame_view = vuba.bgr(frame)
        if p1 is None:
            good_new = None
            good_old = None
        else:    
            good_new = p1[st == 1]
            good_old = self.p0[st == 1]

        if good_new is not None and good_old is not None:
            ind_diff = good_new - good_old
            rot = np.asarray(
                list(map(lambda vals: math.atan2(*np.flip(vals)), ind_diff))
            ) # compute angles of rotation                

            self.point_log.append((good_old, good_new, rot, ind_diff))
            
            for (good_old, good_new, rot, diff) in self.point_log:
                for old, new, r, d in zip(good_old, good_new, rot, diff):
                    if math.sqrt(d[0]**2 + d[1]**2) < 0.25:
                        continue
                    
                    old, new = map(tuple, (old, new))

                    rot_line_color = (0, 255, 0)
                    # if r > 0:
                    #     rot_line_color = (0, 255, 255)

                    new = tuple(map(int, new))
                    old = tuple(map(int, old))
                    cv2.line(frame_view, new, old, rot_line_color, 1)

                if len(good_old) and len(good_new):
                    com_old = good_old.mean(axis=(0,))
                    com_new = good_new.mean(axis=(0,))
                    com_old, com_new = map(tuple, (com_old, com_new))  # for live view

                    com_new = tuple(map(int, com_new))
                    com_old = tuple(map(int, com_old))
                    cv2.line(frame_view, com_new, com_old, (255, 0, 0), 2)

        self.first = frame.copy()

        if p1 is None:
            self.p0 = self.p0.reshape(-1, 1, 2)
        else:
            self.p0 = good_new.reshape(-1, 1, 2)

        #return np.vstack((frame_view, self.rot_mask))
        #resized_mask = cv2.resize(self.rot_mask, (round(self.rot_mask.shape[1]/3), round(self.rot_mask.shape[0]/3)))
        #white_border = np.full((resized_mask.shape[0]+2, resized_mask.shape[1]+2, 3), 255).astype(np.uint8)
        
        #frame_view[:white_border.shape[0], :white_border.shape[1]] = white_border[:]
        #frame_view[:resized_mask.shape[0], :resized_mask.shape[1]] = resized_mask[:]
        #cv2.putText(frame_view, 'Optical Flow Live Stream',
        #            tuple(map(int, (0.01*frame_view.shape[1], 0.02*frame_view.shape[0]))),
        #            font, fontScale, fontColor, lineType)
        return frame_view


# Updated API for Picamera2 ------------------------------------------------------------ #
def get_sensor_modes():
    camera = picamera2.Picamera2()
    modes = camera.sensor_modes
    camera.close()
    return modes


def disable_event():
    pass
    
class TkImageViewer:
    def __init__(self):
        self.root = Tk()
        self.root.title('Video Playback')
        self.lmain = Label(self.root)
        self.lmain.pack()
        self.root.protocol("WM_DELETE_WINDOW", disable_event)

    def show_frame(self, img):
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.root.update()

    def close(self):
        self.root.destroy()


def video_config(sensor_mode, exposure, fps):
    w,h = sensor_mode['size']

    # Correct display aspect ratio
    lores_size = (640,480)
    if (h / w) <= 0.7:
        lores_size = (640,320)
        
    return dict(    
        sensor={"output_size": sensor_mode['size'], "bit_depth": sensor_mode['bit_depth']},
        main={"size": sensor_mode['size'], "format": 'RGB888'},
        lores={"size": lores_size, "format": 'RGB888'},
        controls={
            'ExposureTime': exposure,
            'FrameRate': fps,
            'FrameDurationLimits': (exposure, 1000000),
            'AwbEnable': 0,
            'AeEnable': 0,
            'ColourGains': (0,0)
        })    


def video_capture(path, duration, exposure, fps, sensor_mode=0):
    def encode_func(self, request, name):
        """Performs encoding 

        ***This has been edited to flip the arrays for use with the LEC***

        :param request: Request
        :type request: request
        :param name: Name
        :type name: str
        :return: Jpeg image
        :rtype: bytes
        """
        if self.colour_space is None:
            self.colour_space = self.FORMAT_TABLE[request.config[name]["format"]]
        array = request.make_array(name)
        array = np.flip(array, axis=1)
        return simplejpeg.encode_jpeg(array, quality=self.q, colorspace=self.colour_space,
                                      colorsubsampling=self.colour_subsampling)

    if not path.endswith('.mkv'):
        raise ValueError('MKV file format only currently supported.')

    benchmark = CaptureBenchmark()

    camera = picamera2.Picamera2()
    mode = camera.sensor_modes[sensor_mode]
    config = camera.create_video_configuration(**video_config(mode, exposure, fps))
    camera.configure(config)

    mjpeg_encoder = JpegEncoder(q=80)
    mjpeg_encoder.encode_func = encode_func
    mjpeg_encoder.framerate = fps
    mjpeg_encoder.size = config["main"]["size"]
    mjpeg_encoder.format = config["main"]["format"]
    mjpeg_encoder.output = FfmpegOutput(path)
    mjpeg_encoder.start()        

    im_viewer = TkImageViewer()

    camera.start()
    start = timelib.time()
    benchmark.record_start()
    pg = tqdm(total=duration*fps)
    counter = 0
    while timelib.time() - start < duration:
        request = camera.capture_request()
        mjpeg_encoder.encode("main", request)

        benchmark.record_frame_time()
        benchmark.record_complete()
        
        if counter % (fps // 5) == 0:
            img = request.make_image("lores")
            img = np.flip(img, axis=1)
            im_viewer.show_frame(img)

        request.release()
        pg.update(1)
        counter += 1

    benchmark.record_end()
    mjpeg_encoder.stop()
    camera.stop()
    camera.close()
    im_viewer.close()    

    benchmark.print_log() 
    return benchmark.compute_timings()


def still_capture(exposure, fps, sensor_mode=0):
    camera = picamera2.Picamera2()
    mode = camera.sensor_modes[sensor_mode]
    config = camera.create_video_configuration(**video_config(mode, exposure, fps))
    camera.configure(config)

    # Currently capture according video config, but will change to dedicated still config
    camera.start()
    start = timelib.time()
    while timelib.time() - start < 1: # Capture for 1 second
        request = camera.capture_request()
        img = request.make_array("main")
        request.release()

    img = np.flip(img, axis=1)
    
    camera.stop()   
    camera.close() 
    return img


class LiveStream:
    def __init__(self):
        self.shutdown = False
        self.is_streaming = False
        self.benchmark = CaptureBenchmark()

    def _start(self, exposure, fps, sensor_mode=0):
        self.benchmark.clear()

        camera = picamera2.Picamera2()
        mode = camera.sensor_modes[sensor_mode]
        config = camera.create_video_configuration(**video_config(mode, exposure, fps))
        camera.configure(config)
        print(camera.camera_configuration())
        
        self.shutdown = False
        self.is_streaming = True

        im_viewer = TkImageViewer()

        camera.start()
        self.benchmark.record_start()
        while not self.shutdown:
            request = camera.capture_request()      
            img = request.make_image("lores")
            request.release()

            img = np.flip(img, axis=1)

            im_viewer.show_frame(img)

            self.benchmark.record_frame_time()
            self.benchmark.record_complete()

        self.benchmark.record_end()
        camera.stop()
        camera.close()
        im_viewer.close()    

        self.benchmark.print_log()

    def start(self, exposure, fps, sensor_mode=0):
        thread = threading.Thread(target=self._start, args=(exposure, fps, sensor_mode))
        thread.start()

    def stop(self):
        self.shutdown = True
        self.is_streaming = False


def frame_to_bytes(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes() 


class VideoGenerator:
    def __init__(self, exposure, fps, sensor_mode=0):
        self.camera = picamera2.Picamera2()
        mode = self.camera.sensor_modes[sensor_mode]
        config = self.camera.create_video_configuration(**video_config(mode, exposure, fps))
        self.camera.configure(config)
        print(self.camera.camera_configuration())
        self.benchmark = CaptureBenchmark()

    def __enter__(self):
        self.benchmark.clear()

        self.camera.start()
        self.benchmark.record_start()
        while True:
            request = self.camera.capture_request()      
            img = request.make_array("lores")
            request.release()

            self.benchmark.record_frame_time()
            self.benchmark.record_complete()

            img = np.flip(img, axis=1)

            yield img

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.benchmark.record_end()
        self.camera.stop()
        self.camera.close()
        self.benchmark.print_log()


# This is for the Dash App but is not required for using the above API
class CameraSettings:
    def __init__(self):
        self.settings = {
            'framerate': 30,
            'exposure': 20000, # in u-ms, *1000 for ms
            'sensor_mode': 0
        }

    def get(self, name):
        value = self.settings[name]
        return value

    def set(self, name, value):
        self.settings[name] = value
