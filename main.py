import sys, os
from pytube import YouTube
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt5 import QtGui

class YoutubeDown(QMainWindow):
    def __init__(self):
        super(YoutubeDown, self).__init__()
        self.resize(600,200)
        self.setStyleSheet("QMainWindow {background-color: gray}")
        self.setWindowTitle("mse YouTube video - mp3 Downloader v1.0")

        self.initUI()

    def initUI(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        self.le_link = QLineEdit()
        self.le_link.setClearButtonEnabled(True)
        self.le_link.setStyleSheet("QLineEdit {background-color:pink; margin: 0px 20px; border-radius: 10px}")
        self.le_link.setMinimumSize(300,30)
        self.le_link.setPlaceholderText("YouTube linki")

        self.btn_video = QPushButton("Video indir",self)
        self.btn_video.setStyleSheet("""QPushButton {background-color:pink; border-radius: 10px}""")
        self.btn_video.setMaximumSize(100,30)
        self.btn_video.clicked.connect(self.download)

        self.btn_mp3 = QPushButton("mp3 indir", self)
        self.btn_mp3.setStyleSheet("""QPushButton {background-color:pink; border-radius: 10px}""")
        self.btn_mp3.setMaximumSize(100, 30)
        self.btn_mp3.clicked.connect(self.download)

        vlayout.addWidget(self.le_link)
        hlayout.addWidget(self.btn_mp3)
        hlayout.addWidget(self.btn_video)
        vlayout.addLayout(hlayout)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(vlayout)



    def download(self):
        sender = self.sender().text()
        link = self.le_link.text()
        if link:
            try:
                strim = YouTube(link).streams
                self.statusbar.showMessage("İndirme başladı...", 5000)
                if sender == "mp3 indir":
                    output = strim.filter(type="audio", abr="128kbps")[0].download(output_path="İnen mp3")
                    base, ext = os.path.splitext(output)
                    to_mp3 = base + ".mp3"
                    os.rename(output, to_mp3)
                elif sender == "Video indir":
                    strim.get_highest_resolution().download(output_path="İnen Videolar")

                self.statusbar.showMessage("İndirme bitti.", 10000)
            except Exception as E:
                self.statusbar.showMessage(f"Geçersiz  \t\tHata : {E}", 10000)
                print(E)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QtGui.QFont()
    font.setBold(True)
    font.setFamilies(["Arial"])
    font.setPointSize(11)
    app.setFont(font)
    win = YoutubeDown()
    win.show()
    sys.exit(app.exec_())


