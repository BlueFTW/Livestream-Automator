import subprocess
import time
import os
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMessageBox


# Constants
FOLDER_PATH = 'C:\\Program Files\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg'
STREAM_URL = 'rtmp://live.twitch.tv/app/'

# Add your own accounts here
ACCOUNTS = {
    '1. yung_blue1': {
        'key': 'live_901751223_tDs6rYddK6lqgMZT40nilAtQZTYeR7',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '2. yung_ftw': {
        'key': 'live_901752253_oojyd75Gr4tIButD0Av77ogSLEbmtE',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '3. downem_blue': {
        'key': 'live_901752938_yvONfKvyD1yl5ToScYn3DeIOasrQOo',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '4. yung_atw': {
        'key': 'live_901753515_B9v7M7rGJ1FEhSqDewM3cb3Ryf3ief',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '5. blue_atw': {
        'key': 'live_901754007_MQkQFsJBbHZkyDzTQ94zv6HuKg8N2u',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '6. blueyungin': {
        'key': 'live_901754983_k50sRLwmiSzcxoXtArq7Bh7ULGyqmN',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '7. LindaTheThird': {
        'key': 'live_936569791_bHtaem8nWqkYBkWx8Yb81Z6faYsw3i',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '8. massivemike243': {
        'key': 'live_936572030_RmH4QdmBqXIgNT1GSb6r4O5BeY6mqV',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '9. definitiveselene': {
        'key': 'live_936573143_RCJAdgwfC2KHW3EunIMEVt2aH4iWHc',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '10. thickrick02': {
        'key': 'live_936576426_cIBEFHGj6OzgiZgSX112hTEZieMdlA',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '11. joystickcasey': {
        'key': 'live_936577289_H29UVlAh5VQQIZSxrc44f0vOLZ7VE1',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '12. standardsarah': {
        'key': 'live_937379876_sBMY7FRe4yG3Oo4878TxHyh3TDrsID',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '13. solidsteven00': {
        'key': 'live_937533051_hJowSWawnlDQKWMrixGhIB14O0ckQA',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '14. tallterry': {
        'key': 'live_937535109_v8e9nHGagqwbTDnal1SJIvB3LmrnD1',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '15. colossalcody': {
        'key': 'live_937536493_itkNZne2W5QNXt1UeX3x7026vmsexe',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '16. jumbojim00': {
        'key': 'live_937537689_bOfz5zKSVcSJbFdZrxYT3azAejle1g',
        'url': 'rtmp://live.twitch.tv/app/'
    },

}


VIDEO_PATHS = {
    'Fortnite': 'videos/fortnite.mp4',
    'Minecraft': 'videos/minecraft.mp4',
    'Stardew Valley': 'videos/stardew.mp4',
    'Apex Legends': 'videos/apexlegends.mp4',
    'Fall Guys': 'videos/fallguys.mp4',
    'Animal Crossing': 'videos/animalcrossing.mp4',
    'Persona 5': 'videos/persona5.mp4',
}

QUALITY_PRESETS = {
    'Low Quality (360p)': '600k',
    'Standard Quality (480p)': '1000k',
    'HD Quality (720p)': '2500k',
    'Full HD Quality (1080p)': '4000k',
}


class StreamThread(QThread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.proc = None

    def run(self):
        if subprocess.sys.platform == 'win32':
            self.proc = subprocess.Popen(self.command, shell=True)
        else:
            self.proc = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)
        self.proc.wait()

    def stop(self):
        if self.proc and self.proc.poll() is None:
            if subprocess.sys.platform == 'win32':
                subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.proc.pid), shell=True)
            else:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window setup
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Stream Manager')
        self._configure_styles()

        layout = QVBoxLayout()

        # Progress bar with text
        progress_bar_layout = QHBoxLayout()
        progress_bar_text = QLabel("Streaming Progress:")
        progress_bar_text.setFont(QFont('Arial', 12))
        progress_bar_layout.addWidget(progress_bar_text)
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        progress_bar_layout.addWidget(self.progressBar)
        layout.addLayout(progress_bar_layout)

        # Label for user message
        self.label_user_message = QLabel()
        self.label_user_message.setFont(QFont('Arial', 12))
        layout.addWidget(self.label_user_message)

        # Accounts list widget
        layout.addWidget(self.label_account_select)
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)
        self.listWidget.addItems(list(ACCOUNTS.keys()))
        layout.addWidget(self.listWidget)

        # Stream duration input
        duration_layout = QHBoxLayout()
        self.label_stream_duration = QLabel("Enter the stream duration:")
        self.label_stream_duration.setFont(QFont('Arial', 12))
        duration_layout.addWidget(self.label_stream_duration)
        self.lineEdit_hours = QLineEdit()
        self.lineEdit_hours.setPlaceholderText('Hours')
        duration_layout.addWidget(self.lineEdit_hours)
        self.lineEdit_minutes = QLineEdit()
        self.lineEdit_minutes.setPlaceholderText('Minutes')
        duration_layout.addWidget(self.lineEdit_minutes)
        layout.addLayout(duration_layout)

        # Video selection combo box
        layout.addWidget(self.label_video_select)
        self.comboBox_video = QComboBox()
        self.comboBox_video.addItems(list(VIDEO_PATHS.keys()))
        layout.addWidget(self.comboBox_video)

        # Quality selection combo box
        layout.addWidget(self.label_quality_select)
        self.comboBox_quality = QComboBox()
        self.comboBox_quality.addItems(list(QUALITY_PRESETS.keys()))
        layout.addWidget(self.comboBox_quality)

        # Start button
        self.button_start = QPushButton("Start Streams")
        self.button_start.clicked.connect(self._start_all_streams)
        layout.addWidget(self.button_start)

        # Stop button
        self.button_stop = QPushButton("Stop Streams")
        self.button_stop.clicked.connect(self._stop_all_streams)
        layout.addWidget(self.button_stop)

        # Timer Label
        self.timerLabel = QLabel()
        self.timerLabel.setText("Streaming time: 00:00:00")
        layout.addWidget(self.timerLabel)

        self.setLayout(layout)

        self.processes = {}
        self.start_time = None

        # Configure styles
        self.lineEdit_hours.setStyleSheet("font-size: 16px;")
        self.lineEdit_minutes.setStyleSheet("font-size: 16px;")
        self.comboBox_video.setStyleSheet("font-size: 16px;")
        self.comboBox_quality.setStyleSheet("font-size: 16px;")

    def _configure_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: #f5f5f5;
            }
            QLabel {
                color: #333333;
                font-weight: 500;
            }
            QListWidget {
                background: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px;
                font-size: 16px;
            }
            QListWidget::item:selected {
                background: #ffffff;
                color: #00a6ff;
            }
            QLineEdit {
                background: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px;
                font-weight: 400;
            }
            QComboBox {
                background: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px;
                font-weight: 400;
            }
            QPushButton {
                background: #00a6ff;
                color: #ffffff;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #0085eb;
            }
        """)

        self.label_account_select = QLabel("Select accounts for streaming:")
        self.label_account_select.setFont(QFont('Arial', 12))
        self.label_stream_duration = QLabel("Enter the stream duration:")
        self.label_stream_duration.setFont(QFont('Arial', 12))
        self.label_video_select = QLabel("Select a video for streaming:")
        self.label_video_select.setFont(QFont('Arial', 12))
        self.label_quality_select = QLabel("Select video quality:")
        self.label_quality_select.setFont(QFont('Arial', 12))

    def _start_all_streams(self):
        hours = self.lineEdit_hours.text()
        minutes = self.lineEdit_minutes.text()

        # Validate hours and minutes, replace with 0 if empty
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0

        duration_in_seconds = (hours * 3600) + (minutes * 60)
        video_key = self.comboBox_video.currentText()
        video_path = VIDEO_PATHS[video_key]
        quality_key = self.comboBox_quality.currentText()
        bitrate = QUALITY_PRESETS[quality_key]

        # Update user message label
        num_accounts = len(self.listWidget.selectedItems())
        duration_time = f"{hours} hours and {minutes} minutes" if hours > 0 and minutes > 0 else (
            f"{hours} hours" if hours > 0 else f"{minutes} minutes")
        self.label_user_message.setText(f"{num_accounts} accounts are going live for {duration_time}")

        # Update progress bar maximum value
        self.progressBar.setMaximum(duration_in_seconds)
        self.progressBar.setValue(0)

        for item in self.listWidget.selectedItems():
            account_key = item.text()
            account_info = ACCOUNTS[account_key]
            stream_url = f'{account_info["url"]}{account_info["key"]}'
            command = f'"{FOLDER_PATH}" -re -i "{video_path}" -t {duration_in_seconds} -c:v libx264 -b:v {bitrate} -pix_fmt yuv420p -f flv "{stream_url}"'
            thread = StreamThread(command)
            thread.start()

            self.processes[account_key] = thread
            self.start_time = time.time()

        # Start a timer to update the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_progress_bar_and_timer)
        self.timer.start(1000)  # Update every second

    def _update_progress_bar_and_timer(self):
        # Increment progress bar value
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + 1)

        # Update the timer label
        elapsed_time = int(time.time() - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timerLabel.setText(f"Streaming time: {hours:02}:{minutes:02}:{seconds:02}")

        # Check if the progress bar is full
        if current_value + 1 >= self.progressBar.maximum():
            self._stop_all_streams()
            self._on_streaming_time_end()

    def _check_streaming_time_end(self):
        elapsed_time = int(time.time() - self.start_time)
        if elapsed_time >= self.progressBar.maximum():
            self._on_streaming_time_end()

    def _on_streaming_time_end(self):
        # Stop timer
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Clear threads
        self.processes = {}

        # Reset progress bar
        self.progressBar.setValue(0)

        # Show a popup message
        QMessageBox.information(self, "Streaming Ended", "Stream(s) completed. The streaming time has been reached.")

    def _stop_all_streams(self):
        for thread in self.processes.values():
            thread.stop()
        self.processes.clear()  # Clear the processes
        self.label_user_message.setText("All streams stopped.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()