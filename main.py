import time
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Constants
FOLDER_PATH = 'C:\\Program Files\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg'
VIDEO_PATH = 'C:\\Users\\YourName\\Downloads\\Filename.mp4'
STREAM_URL = 'rtmp://live.twitch.tv/app/'

# Add your own accounts here
ACCOUNTS = {
    '1. yung_blue1': 'live_901751223_tDs6rYddK6lqgMZT40nilAtQZTYeR7',
    '2. yung_ftw': 'live_901752253_oojyd75Gr4tIButD0Av77ogSLEbmtE',
    '3. downem_blue': 'live_901752938_yvONfKvyD1yl5ToScYn3DeIOasrQOo',
    '4. yung_atw': 'live_901753515_B9v7M7rGJ1FEhSqDewM3cb3Ryf3ief',
    '5. blue_atw': 'live_901754007_MQkQFsJBbHZkyDzTQ94zv6HuKg8N2u',
    '6. blueyungin': 'live_901754983_k50sRLwmiSzcxoXtArq7Bh7ULGyqmN',
}


# Helper function to start stream
def start_stream(account_name, stream_key, duration):
    command = f'"{FOLDER_PATH}" -re -i "{VIDEO_PATH}" -c:v copy -c:a aac -strict -2 -f flv "{STREAM_URL}{stream_key}"'
    proc = subprocess.Popen(command, shell=True)
    time.sleep(duration)  # Stream for the specified duration in seconds
    proc.terminate()  # Terminate the process after the duration ends

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window setup
        self.setGeometry(300, 300, 400, 350)
        self.setWindowTitle('Stream Manager')
        self._configure_styles()

        layout = QVBoxLayout()

        # Accounts list widget
        self.listWidget = QListWidget()
        self.listWidget.setFocusPolicy(Qt.NoFocus)
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)
        self.listWidget.itemSelectionChanged.connect(self._update_account_selections)
        self.listWidget.addItems(list(ACCOUNTS.keys()))
        layout.addWidget(self.label_account_select)
        layout.addWidget(self.listWidget)

        # Stream duration input
        layout.addWidget(self.label_stream_duration)
        self.lineEdit = QLineEdit()
        layout.addWidget(self.lineEdit)

        # Start button
        self.button = QPushButton("Start Streams")
        self.button.clicked.connect(self._start_all_streams)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _configure_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: #f5f5f5;
            }
            QLabel {
                color: #333333;
                font-weight: 500;
                text-align: center;
            }
            QListWidget {
                background: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                padding: 5px;
                font-size: 16px;
                outline: 0;
            }
            QListWidget::item {
                outline: 0;
            }   
            QListWidget::item:selected {
                background: #ffffff;
                color: #00a6ff;
                outline: 0;
            }
            QLineEdit {
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

        self.label_stream_duration = QLabel("Enter the stream duration in hours:")
        self.label_stream_duration.setFont(QFont('Arial', 12))

    def _update_account_selections(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            base_name = self._get_base_account_name(item.text())
            if base_name in [self._get_base_account_name(x.text()) for x in self.listWidget.selectedItems()]:
                item.setText(f'✓ {base_name}')
            else:
                item.setText(base_name)

    def _get_base_account_name(self, account_name):
        return account_name[2:] if account_name.startswith('✓ ') else account_name

    def _start_all_streams(self):
        duration_seconds = float(self.lineEdit.text()) * 60 * 60
        selected_accounts = [self._get_base_account_name(item.text()) for item in self.listWidget.selectedItems()]
        if selected_accounts:
            for account_name in selected_accounts:
                start_stream(account_name, ACCOUNTS[account_name], duration_seconds)
            print("All streams have started. Running for the specified duration...")
        else:
            print("No account selected. Please select at least one account.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()










