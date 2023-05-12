from PyQt5.QtCore import pyqtSignal, QThread
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication
import asyncio
from asyncqt import QEventLoop, asyncSlot
from mavsdk import System
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QColor
import time
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    finding_signal = pyqtSignal(str)
    def __init__(self, port, direct):
        super().__init__()
        self.port = port
        self.direct = direct
    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.direct)
        while True:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, cv_img = cap.read()
            #cv_img = cv2.flip(cv_img, 1)
            if self.findFace(cv_img):
                self.finding_signal.emit(str(self.port)+"Found!!!")

            else:
                self.finding_signal.emit(str(self.port)+"Finding ...")
            if ret:
                self.change_pixmap_signal.emit(cv_img)


    def findFace(self, img):
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True
        return False


