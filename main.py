import subprocess
import time
import os
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMessageBox
from constants import FOLDER_PATH, STREAM_URL, ACCOUNTS, VIDEO_PATHS, QUALITY_PRESETS


class StreamThread(QThread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.proc = None

    def run(self):
        try:
            if subprocess.sys.platform == 'win32':
                self.proc = subprocess.Popen(self.command, shell=True)
            else:
                self.proc = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)
            self.proc.wait()
        except Exception as e:
            print(f"Error in stream thread: {e}")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            try:
                if subprocess.sys.platform == 'win32':
                    subprocess.Popen(f"TASKKILL /F /PID {self.proc.pid} /T", shell=True)
                else:
                    os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            except Exception as e:
                print(f"Error while stopping stream: {e}")


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
        self.timer.timeout.connect(self._check_streaming_time_end)
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

            # Stop all streams gracefully
        self._stop_all_streams()

        # Reset progress bar
        self.progressBar.setValue(0)

        # Show a popup message
        QMessageBox.information(self, "Streaming Ended", "Stream(s) completed. The streaming time has been reached.")

    def _stop_all_streams(self):
        for thread in self.processes.values():
            thread.stop()
            thread.wait()
        self.processes.clear()  # Clear the processes
        self.label_user_message.setText("All streams stopped.")
        # Stop the timer that checks streaming time end
        if hasattr(self, 'timer'):
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()