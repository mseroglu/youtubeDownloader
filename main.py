import sys, os
from pytube import YouTube, Playlist
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt5 import QtGui
from threading import Thread

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

        self.label = QLabel("Oynatma listesinin tümünü indirmek için listenin linkini giriniz.\n"
                            "Bu işlem uzun sürebilir.")
        self.label.setMaximumSize(600,40)
        self.label.setStyleSheet("""QLabel {background-color:pink; padding:5px 10px; margin: 0px 20px; border-radius: 10px;}
                                    QLabel:hover {background-color:green;}""")

        self.le_link = QLineEdit()
        self.le_link.setClearButtonEnabled(True)
        self.le_link.setStyleSheet("QLineEdit {background-color:pink; padding:5px 10px; margin: 0px 20px; border-radius: 10px}")
        self.le_link.setMinimumSize(300,30)
        self.le_link.setPlaceholderText("Video linki veya Oynatma Listesi linki")

        self.btn_video = QPushButton("Video indir",self)
        self.btn_video.setStyleSheet("""QPushButton {background-color:pink; border-radius: 10px}
                                        QPushButton:hover {background-color:red; border-radius: 10px}""")
        self.btn_video.setMaximumSize(100,30)
        self.btn_video.clicked.connect(self.download)

        self.btn_mp3 = QPushButton("mp3 indir", self)
        self.btn_mp3.setStyleSheet("""QPushButton {background-color:pink; border-radius: 10px}""")
        self.btn_mp3.setMaximumSize(100, 30)
        self.btn_mp3.clicked.connect(self.downloadWithTread)

        vlayout.addWidget(self.label)
        vlayout.addWidget(self.le_link)
        hlayout.addWidget(self.btn_mp3)
        hlayout.addWidget(self.btn_video)
        vlayout.addLayout(hlayout)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(vlayout)

    def downloadWithTread(self):
        Thread(target=self.download).start()

    def getDownloadLinksOnPlaylist(self) -> list :
        try:
            link = self.le_link.text()
            if link:
                pl = Playlist(link)
                print(pl)               # bu print durmalı, excepte düşmek için
                return pl
        except Exception as E:
            return [link,]

    def download(self):
        try:
            sender = self.sender().text()
            linkListesi = self.getDownloadLinksOnPlaylist()
            if linkListesi:
                count = 0
                for link in linkListesi:
                    strim = YouTube(link).streams
                    if sender == "mp3 indir":
                        output = strim.filter(type="audio", abr="128kbps")[0].download(output_path="Download Music")
                        base, ext = os.path.splitext(output)
                        to_mp3 = base + ".mp3"
                        os.rename(output, to_mp3)
                    elif sender == "Video indir":
                        strim.get_highest_resolution().download(output_path="Download Video")
                    count +=1
                    self.statusbar.showMessage(f"{count} indirme tamamlandı.")
                self.statusbar.showMessage(f"{count} indirme yapıldı. İşlem tamamlandı.")
        except Exception as E:
            self.statusbar.showMessage(f"Geçersiz bir link girdiniz !!!", 10000)
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


#------------------- pyinstaller --noconsole --onefile -i "youtube.ico" main.py ------------------#