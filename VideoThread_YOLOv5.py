from PyQt5.QtCore import pyqtSignal, QThread
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication
import asyncio
from asyncqt import QEventLoop, asyncSlot
from mavsdk import System
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QColor
from time import time
import torch


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    finding_signal = pyqtSignal(str)

    def __init__(self, port, direct):
        super().__init__()
        self.device = None
        self.out_file = None
        self.model = None
        self.classes = None
        self.port = port
        self.direct = direct

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.direct)
        self.model = torch.hub.load('yolov5', 'custom', path='yolov5s.pt')
        self.model.classes = [0]
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        while True:
            start_time = time()
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, cv_img = cap.read()
            # cv_img = cv2.flip(cv_img, 1)
            results = self.score_frame(cv_img)
            label, cv_img = self.plot_boxes(results, cv_img)
            if 0 in label:
                self.finding_signal.emit(str(self.port)+"Found!!!")
                # print(str(self.port)+" Found!!!")
            else:
                self.finding_signal.emit(str(self.port)+"Finding ...")

            if ret:
                self.change_pixmap_signal.emit(cv_img)
            end_time = time()
            fps = 1 / (np.round(end_time - start_time, 3))
            # print(f"Frames Per Second : {round(fps, 2)} FPS")

    def findFace(self, img):
        faceCascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True
        return False

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -
                                        1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            # print("ddd", round(cord[i][4], 2))
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]) + " " + str(round(row[4], 2)), (x1, y1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                # print(f"label ={labels}")

        return labels, frame
