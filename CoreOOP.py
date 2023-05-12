import asyncio

from GUI import *
from VideoThread import *
from ui_functions import *

NUM_DRONE_CONNECTED = 0
INF = float('inf')

NUM_DRONES = 3

drone_1 = System(mavsdk_server_address="localhost", port=50060)
drone_2 = System(mavsdk_server_address="localhost", port=50061)
drone_3 = System(mavsdk_server_address="localhost", port=50062)

direct_person       = "VidTest/Test1.mp4"
# direct_person       = 0
direct_nonPerson_1  = "VidTest/NonPerson2.mp4"
direct_nonPerson_2  = "VidTest/NonPerson2.mp4"

class My_UI(QMainWindow):
    signal_found = pyqtSignal(str)
    """Khoi tao"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Default Signal
        self.signal_default = ["Finding ..."] * NUM_DRONES
        # Handle Target

        # Flag
        self.flag = [0] * NUM_DRONES
        # Flag Connect
        self.flag_connect = [0] * NUM_DRONES
        # Signal from Drone
        self.signal_finding = ["Finding ..."] * NUM_DRONES
        # create a grey pixmap
        grey = QPixmap(self.ui.webcam_drone_1.geometry().width(), self.ui.webcam_drone_1.geometry().height())
        grey.fill(QColor('darkGray'))
        # create list_position
        self.list_position = [0] * 3
        # create matrix distance
        self.matrix_distance = [[INF, INF, INF],[INF, INF, INF], [INF, INF, INF]]
        # create list num lief packages
        self.list_num_rescue_packages = [0] * NUM_DRONES
        # set the image to the grey pixmap
        """Webcam 1"""
        self.ui.webcam_drone_1.setPixmap(grey)
        self.ui.webcam_drone_1.setText("Waiting Signal from Drone1's Camera")
        """Webcam 2"""
        self.ui.webcam_drone_2.setPixmap(grey)
        self.ui.webcam_drone_2.setText("Waiting Signal from Drone2's Camera")
        """Webcam 3"""
        self.ui.webcam_drone_3.setPixmap(grey)
        self.ui.webcam_drone_3.setText("Waiting Signal from Drone3's Camera")

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.Btn_drone_1.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_1))
        """Button"""

        self.ui.BtnConnect_1.clicked.connect(self.Connect_Drone_1)

        self.ui.Arm_1.clicked.connect(self.Arm_1)

        self.ui.DisArm_1.clicked.connect(self.DisArm_1)

        self.ui.TakeOff_1.clicked.connect(self.TakeOff_1)

        self.ui.Landing_1.clicked.connect(self.Landing_1)

        self.ui.RTL_1.clicked.connect(self.RTL_1)
        """Window contain Video"""
        # create the video capture thread
        self.thread = VideoThread(0, direct_person)
        # start the thread
        self.thread.start()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # connect its signal finding to the label
        self.thread.finding_signal.connect(self.update_signal)

        ######################################################################################
        # PAGE 2
        self.ui.Btn_drone_2.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_2))
        """Button"""

        self.ui.BtnConnect_2.clicked.connect(self.Connect_Drone_2)

        self.ui.Arm_2.clicked.connect(self.Arm_2)

        self.ui.DisArm_2.clicked.connect(self.DisArm_2)

        self.ui.TakeOff_2.clicked.connect(self.TakeOff_2)

        self.ui.Landing_2.clicked.connect(self.Landing_2)

        self.ui.RTL_2.clicked.connect(self.RTL_2)
        """Window contain Video"""
        # create the video capture thread
        self.thread_1 = VideoThread(1, direct_nonPerson_1)
        # start the thread
        self.thread_1.start()
        # connect its signal to the update_image slot
        self.thread_1.change_pixmap_signal.connect(self.update_image_1)
        # connect its signal finding to the label
        self.thread_1.finding_signal.connect(self.update_signal)
        # PAGE 3
        self.ui.Btn_drone_3.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_3))
        """Button"""

        self.ui.BtnConnect_3.clicked.connect(self.Connect_Drone_3)

        self.ui.Arm_3.clicked.connect(self.Arm_3)

        self.ui.DisArm_3.clicked.connect(self.DisArm_3)

        self.ui.TakeOff_3.clicked.connect(self.TakeOff_3)

        self.ui.Landing_3.clicked.connect(self.Landing_3)

        self.ui.RTL_3.clicked.connect(self.RTL_3)
        """Window contain Video"""
        # create the video capture thread
        self.thread_2 = VideoThread(2, direct_nonPerson_2)
        # start the thread
        self.thread_2.start()
        # connect its signal to the update_image slot
        self.thread_2.change_pixmap_signal.connect(self.update_image_2)
        # connect its signal finding to the label
        self.thread_2.finding_signal.connect(self.update_signal)

        # PAGE Camera
        self.ui.Btn_Camera.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_camera))


    ####################################################################################################################
    @pyqtSlot(str)
    def update_signal(self, signal):
        """Updates the image_label with a new opencv image"""
        if(signal[0] == '0'):
            if(signal[1:] == "Found!!!"):
                self.ui.finding_1.setStyleSheet("color: rgb(0,255,0);")
                self.ui.label_drone_4.setStyleSheet("color: rgb(0,255,0);")
            else:
                self.ui.finding_1.setStyleSheet("color: rgb(255,0,0);")
                self.ui.label_drone_4.setStyleSheet("color: rgb(255,0,0);")
            self.ui.finding_1.setText(signal[1:])
            self.signal_finding[0] = self.ui.finding_1.text()

        if (signal[0] == '1'):
            if (signal[1:] == "Found!!!"):
                self.ui.finding_2.setStyleSheet("color: rgb(0,255,0);")
                self.ui.label_drone_5.setStyleSheet("color: rgb(0,255,0);")
            else:
                self.ui.finding_2.setStyleSheet("color: rgb(255,0,0);")
                self.ui.label_drone_5.setStyleSheet("color: rgb(255,0,0);")
            self.ui.finding_2.setText(signal[1:])
            self.signal_finding[1] = self.ui.finding_2.text()

        if (signal[0] == '2'):
            if (signal[1:] == "Found!!!"):
                self.ui.finding_3.setStyleSheet("color: rgb(0,255,0);")
                self.ui.label_drone_6.setStyleSheet("color: rgb(0,255,0);")
            else:
                self.ui.finding_3.setStyleSheet("color: rgb(255,0,0);")
                self.ui.label_drone_5.setStyleSheet("color: rgb(255,0,0);")
            self.ui.finding_3.setText(signal[1:])
            self.signal_finding[2] = self.ui.finding_3.text()
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.webcam_drone_1.setPixmap(qt_img)
        self.ui.Monitor_drone_1.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_image_1(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.webcam_drone_2.setPixmap(qt_img)
        self.ui.Monitor_drone_2.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_image_2(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.webcam_drone_3.setPixmap(qt_img)
        self.ui.Monitor_drone_3.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.webcam_drone_1.geometry().width(),
                                        self.ui.webcam_drone_1.geometry().height(),
                                        Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    ####################################################################################################################
    """Ket noi"""
    # Drone 1
    @asyncSlot()
    async def Connect_Drone_1(self):
        global drone_1, NUM_DRONE_CONNECTED
        print("--Connecting to Drone")
        await drone_1.connect()
        print("--Drone Connected")

        self.ui.WaitingConnection_1.setText("Drone1 connected")
        self.ui.WaitingConnection_1.setStyleSheet("color: rgb(0,255,0);")
        self.list_num_rescue_packages[0] = int(self.ui.plainText_num_packet_1.toPlainText())
        await asyncio.gather(self.get_alt_1(), self.get_arm_1(), self.get_batt_1(), self.get_mode_1(), self.get_gps_1(),
                             self.print_status_text_1(),
                             self.loading_signal_cam_1(),
                             self.Compute_Distance())
        return None
    # Drone 2
    @asyncSlot()
    async def Connect_Drone_2(self):
        global drone_2, NUM_DRONE_CONNECTED
        print("--Connecting to Drone")
        await drone_2.connect()
        print("--Drone Connected")

        self.ui.WaitingConnection_2.setText("Drone2 connected")
        self.ui.WaitingConnection_2.setStyleSheet("color: rgb(0,255,0);")
        self.list_num_rescue_packages[1] = int(self.ui.plainText_num_packet_2.toPlainText())
        await asyncio.gather(self.get_alt_2(), self.get_arm_2(), self.get_batt_2(), self.get_mode_2(), self.get_gps_2(),
                             self.print_status_text_2(),
                             self.loading_signal_cam_2())
        return None

    # Drone 3
    @asyncSlot()
    async def Connect_Drone_3(self):
        global drone_3, NUM_DRONE_CONNECTED
        print("--Connecting to Drone")
        await drone_3.connect()
        print("--Drone Connected")

        self.ui.WaitingConnection_3.setText("Drone3 connected")
        self.ui.WaitingConnection_3.setStyleSheet("color: rgb(0,255,0);")
        self.list_num_rescue_packages[2] = int(self.ui.plainText_num_packet_3.toPlainText())
        await asyncio.gather(self.get_alt_3(), self.get_arm_3(), self.get_batt_3(), self.get_mode_3(),
                             self.get_gps_3(),
                             self.print_status_text_3(),
                             self.loading_signal_cam_3())
        return None
    ####################################################################################################################
    """To hop cac ham lay thong tin"""
    # Drone 1
    @asyncSlot()
    async def get_alt_1(self):
        global NUM_DRONE_CONNECTED
        async for position in drone_1.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_1.setText(str(alt_rel)+" m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_1.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_1.setText(str(latitude))
            self.ui.longitude_1.setText(str(longitude))
            self.list_position[0] = [latitude, longitude]
            if self.flag_connect[0] == 0:
                NUM_DRONE_CONNECTED += 1
                self.flag_connect[0] = 1
        return None

    @asyncSlot()
    async def get_mode_1(self):
        async for mode in drone_1.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_1.setText(mod)
        return None

    @asyncSlot()
    async def get_batt_1(self):
        async for batt in drone_1.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_1.setText(str(v) + " V")
            self.ui.Batt_Rem_1.setText(str(rem) + " %")
        return None

    @asyncSlot()
    async def get_arm_1(self):
        async for arm in drone_1.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_1.setText(armed)
        return None

    @asyncSlot()
    async def get_gps_1(self):
        async for gps in drone_1.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_1.setText(str(gps_fix))
            self.ui.Sat_Num_1.setText(str(sat))

    @asyncSlot()
    async def print_status_text_1(self):
        async for status_text in drone_1.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.plainTextEdit_1.appendPlainText(Status_Text)


    @asyncSlot()
    async def loading_signal_cam_1(self):
        await asyncio.sleep(2)
        while True:
            for index, signal in enumerate(self.signal_finding):
                if signal == "Found!!!" or self.flag[0] == 1:
                    distance = self.matrix_distance[index][0]
                    if distance <0.0009 and self.flag[0] == 1:
                        self.list_num_rescue_packages[0] -= 1
                        self.ui.plainText_num_packet_1.setPlainText(str(self.list_num_rescue_packages[0]))
                        self.flag[0] = 0
                    if signal != self.signal_default[0]:
                        if self.signal_default[0] == "Finding ...":
                            self.signal_default[0] = signal
                            if distance == min(self.matrix_distance[index]) and self.list_num_rescue_packages[0] != 0 and self.list_num_rescue_packages[index] == 0:
                                await self.Move_To_Target_1(index)
                                self.flag[0] = 1
                            if index == 0:
                                await self.Move_To_Target_1(index)
                                if self.list_num_rescue_packages[0] != 0: self.flag[0] = 1
                        else:
                            self.signal_default[0] = signal
                    break
                if index == NUM_DRONES - 1 and signal == "Finding ...":
                    self.signal_default[0] = signal
            await asyncio.sleep(1)
    # Drone 2
    @asyncSlot()
    async def get_alt_2(self):
        global NUM_DRONE_CONNECTED
        async for position in drone_2.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_2.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_2.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_2.setText(str(latitude))
            self.ui.longitude_2.setText(str(longitude))
            self.list_position[1] = [latitude, longitude]
            if self.flag_connect[1] == 0:
                NUM_DRONE_CONNECTED += 1
                self.flag_connect[1] = 1
        return None

    @asyncSlot()
    async def get_mode_2(self):
        async for mode in drone_2.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_2.setText(mod)
        return None

    @asyncSlot()
    async def get_batt_2(self):
        async for batt in drone_2.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_2.setText(str(v) + " V")
            self.ui.Batt_Rem_2.setText(str(rem) + " %")
        return None

    @asyncSlot()
    async def get_arm_2(self):
        async for arm in drone_2.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_2.setText(armed)
        return None

    @asyncSlot()
    async def get_gps_2(self):
        async for gps in drone_2.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_2.setText(str(gps_fix))
            self.ui.Sat_Num_2.setText(str(sat))

    @asyncSlot()
    async def print_status_text_2(self):
        async for status_text in drone_2.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.plainTextEdit_2.appendPlainText(Status_Text)

    @asyncSlot()
    async def loading_signal_cam_2(self):
        await asyncio.sleep(2)
        while True:

            # if self.list_num_rescue_packages[1] == 0:
            #
            #     print("Drone 2 out of rescue packages")
            # else:
            for index, signal in enumerate(self.signal_finding):
                if signal == "Found!!!" or self.flag[1] == 1:
                    distance = self.matrix_distance[index][1]

                    if distance < 0.0009 and self.flag[1] == 1:
                        self.list_num_rescue_packages[1] -= 1
                        self.ui.plainText_num_packet_2.setPlainText(str(self.list_num_rescue_packages[1]))
                        self.flag[1] = 0

                    if signal != self.signal_default[1]:
                        if self.signal_default[1] == "Finding ...":
                            self.signal_default[1] = signal
                            if distance == min(self.matrix_distance[index]) and self.list_num_rescue_packages[1] != 0 and self.list_num_rescue_packages[index] == 0:
                                await self.Move_To_Target_2(index)
                                self.flag[1] = 1
                            if index == 1 :
                                await self.Move_To_Target_2(index)
                                if self.list_num_rescue_packages[1] != 0: self.flag[1] = 1
                        else:
                            self.signal_default[1] = signal
                    break
                if index == NUM_DRONES - 1 and signal == "Finding ...":
                    self.signal_default[1] = signal
            await asyncio.sleep(1)

    # Drone 3
    @asyncSlot()
    async def get_alt_3(self):
        global NUM_DRONE_CONNECTED
        async for position in drone_3.telemetry.position():
            alt_rel = round(position.relative_altitude_m, 1)
            self.ui.Alt_Rel_3.setText(str(alt_rel) + " m")

            alt_msl = round(position.absolute_altitude_m, 1)
            self.ui.Alt_MSL_3.setText(str(alt_msl) + " m")

            latitude, longitude = position.latitude_deg, position.longitude_deg
            self.ui.latitude_3.setText(str(latitude))
            self.ui.longitude_3.setText(str(longitude))
            self.list_position[2] = [latitude, longitude]
            if self.flag_connect[2] == 0:
                NUM_DRONE_CONNECTED += 1
                self.flag_connect[2] = 1
        return None

    @asyncSlot()
    async def get_mode_3(self):
        async for mode in drone_3.telemetry.flight_mode():
            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.Mode_3.setText(mod)
        return None

    @asyncSlot()
    async def get_batt_3(self):
        async for batt in drone_3.telemetry.battery():
            v = round(batt.voltage_v, 1)
            rem = round(100 * batt.remaining_percent, 1)

            self.ui.Batt_V_3.setText(str(v) + " V")
            self.ui.Batt_Rem_3.setText(str(rem) + " %")
        return None

    @asyncSlot()
    async def get_arm_3(self):
        async for arm in drone_3.telemetry.armed():
            armed = "ARMED" if arm else "Disarmed"
            self.ui.ArmStatus_3.setText(armed)
        return None

    @asyncSlot()
    async def get_gps_3(self):
        async for gps in drone_3.telemetry.gps_info():
            sat = gps.num_satellites
            gps_fix = gps.fix_type

            self.ui.GPS_Fix_3.setText(str(gps_fix))
            self.ui.Sat_Num_3.setText(str(sat))

    @asyncSlot()
    async def print_status_text_3(self):
        async for status_text in drone_3.telemetry.status_text():
            Status_Text = f"Status: {status_text.type}: {status_text.text}\n"
            self.ui.plainTextEdit_3.appendPlainText(Status_Text)

    @asyncSlot()
    async def loading_signal_cam_3(self):
        await asyncio.sleep(2)
        while True:

            # if self.list_num_rescue_packages[2] == 0:
            #     print("Drone 3 out of rescue packages")
            #
            # else:
            for index, signal in enumerate(self.signal_finding):
                if signal == "Found!!!" or self.flag[2] == 1:
                    distance = self.matrix_distance[index][2]
                    if distance < 0.0009 and self.flag[2] == 1:
                        self.list_num_rescue_packages[2] -= 1
                        self.ui.plainText_num_packet_3.setPlainText(str(self.list_num_rescue_packages[2]))
                        self.flag[2] = 0

                    if signal != self.signal_default[2]:
                        if self.signal_default[2] == "Finding ...":
                            self.signal_default[2] = signal
                            if distance == min(self.matrix_distance[index]) and self.list_num_rescue_packages[2] != 0 and self.list_num_rescue_packages[index] == 0:
                                await self.Move_To_Target_3(index)
                                self.flag[2] = 1
                            if index == 2 :
                                await self.Move_To_Target_3(index)
                                if self.list_num_rescue_packages[2] != 0: self.flag[2] = 1
                        else:
                            self.signal_default[2] = signal
                    break
                if index == NUM_DRONES - 1 and signal == "Finding ...":
                    self.signal_default[2] = signal
            await asyncio.sleep(1)
    ####################################################################################################################
    """To hop cac ham dieu khien"""
    """ Drone 1"""
    @asyncSlot()
    async def DisArm_1(self):
        print("--Disarming Drone...")
        await drone_1.action.disarm()
        print("--Drone disarmed...")

    @asyncSlot()
    async def Arm_1(self):
        print("--Arming Drone...")
        await drone_1.action.arm()
        print("--Drone Armed...")

    @asyncSlot()
    async def TakeOff_1(self):
        print("--Taking off...")
        await drone_1.action.takeoff()

    @asyncSlot()
    async def RTL_1(self):
        await drone_1.action.set_return_to_launch_altitude(2)
        await drone_1.action.return_to_launch()
        print("--Returning to launch...")

    @asyncSlot()
    async def Landing_1(self):
        await drone_1.action.land()
        print("--Landing...")

    @asyncSlot()
    async def Move_To_Target_1(self, index):
        target = self.list_position[index]
        # To fly drone 20m above the ground plane
        flying_alt = float(self.ui.Alt_MSL_1.text()[:-2])
        # goto_location() takes Absolute MSL altitude
        await drone_1.action.goto_location(target[0], target[1], flying_alt, 0)
        print("--Drone 1 is arriving to the target")

    """Drone 2"""
    @asyncSlot()
    async def DisArm_2(self):
        print("--Disarming Drone...")
        await drone_2.action.disarm()
        print("--Drone disarmed...")

    @asyncSlot()
    async def Arm_2(self):
        print("--Arming Drone...")
        await drone_2.action.arm()
        print("--Drone Armed...")

    @asyncSlot()
    async def TakeOff_2(self):
        print("--Taking off...")
        await drone_2.action.takeoff()

    @asyncSlot()
    async def RTL_2(self):
        await drone_2.action.set_return_to_launch_altitude(2)
        await drone_2.action.return_to_launch()
        print("--Returning to launch...")

    @asyncSlot()
    async def Move_To_Target_2(self, index):
        target = self.list_position[index]
        # To fly drone 20m above the ground plane
        flying_alt = float(self.ui.Alt_MSL_2.text()[:-2])
        # goto_location() takes Absolute MSL altitude
        await drone_2.action.goto_location(target[0], target[1], flying_alt, 0)
        print("--Drone 2 is arriving to the target")

    @asyncSlot()
    async def Landing_2(self):
        await drone_2.action.land()
        print("--Landing...")

    """Drone 3"""
    @asyncSlot()
    async def DisArm_3(self):
        print("--Disarming Drone...")
        await drone_3.action.disarm()
        print("--Drone disarmed...")

    @asyncSlot()
    async def Arm_3(self):
        print("--Arming Drone...")
        await drone_3.action.arm()
        print("--Drone Armed...")

    @asyncSlot()
    async def TakeOff_3(self):
        print("--Taking off...")
        await drone_3.action.takeoff()

    @asyncSlot()
    async def RTL_3(self):
        await drone_3.action.set_return_to_launch_altitude(2)
        await drone_3.action.return_to_launch()
        print("--Returning to launch...")

    @asyncSlot()
    async def Move_To_Target_3(self, index):
        target = self.list_position[index]
        # To fly drone 20m above the ground plane
        flying_alt = float(self.ui.Alt_MSL_3.text()[:-2])
        # goto_location() takes Absolute MSL altitude
        await drone_3.action.goto_location(target[0], target[1], flying_alt, 0)
        print("--Drone 3 is arriving to the target")

    @asyncSlot()
    async def Landing_3(self):
        await drone_3.action.land()
        print("--Landing...")

    """Compute distance"""
    @asyncSlot()
    async def Compute_Distance(self):
        while True:
            if(NUM_DRONE_CONNECTED == 3):
                for i in range(NUM_DRONES):
                    for j in range(i, NUM_DRONES):
                        if j == i:
                            self.matrix_distance[i][j] = 0 if self.list_num_rescue_packages[j] != 0 else INF
                        else:
                            start_lat, start_log = self.list_position[i]
                            target_lat, target_log = self.list_position[j]

                            # print(start_lat, start_log , target_lat, target_log)
                            distance = getDistanceBetweenPointsNew(start_lat, start_log, target_lat, target_log,
                                                                   "kilometers")

                            self.matrix_distance[i][j] = distance if self.list_num_rescue_packages[j] != 0 else INF
                            self.matrix_distance[j][i] = distance if self.list_num_rescue_packages[i] != 0 else INF
                        # print(f'i: {i}, j: {j}, ',self.matrix_distance[i][j])
                # for i in range(NUM_DRONES):
                #     for j in range(NUM_DRONES):
                #         print(self.matrix_distance[i][j], end=" ")
                #     print()
                # print("*****************************")
            await asyncio.sleep(1)
    ####################################################################################################################

class UIFunctions(My_UI):

    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()