import sys, os
from pytube import YouTube, Playlist
from PyQt5.QtWidgets import QMainWindow, QApplication, QProgressBar, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt5 import QtGui
from threading import Thread
from multiprocessing import Process


def downloadWithTread():
    global win
    try:
        t1 = Thread(target=win.download)
        t1.start()
    except Exception as E:
        print(E)


class YoutubeDown(QMainWindow):
    def __init__(self):
        super(YoutubeDown, self).__init__()
        try:
            self.resize(600,300)
            self.setStyleSheet("QMainWindow {background-color: gray}")
            self.setWindowTitle("mse YouTube video - mp3 Downloader v1.0")

            self.initUI()
        except Exception as E:
            print(E)

    def initUI(self):
        try:
            self.statusbar = QStatusBar()
            self.setStatusBar(self.statusbar)
            vlayout = QVBoxLayout()
            hlayout = QHBoxLayout()

            self.label = QLabel("Oynatma listesinin tümünü indirmek için listenin linkini giriniz.\n"
                                "Bu işlem uzun sürebilir.")
            self.label.setMaximumSize(600,60)
            self.label.setStyleSheet("""QLabel {background-color: #8f7486; color:white; padding:5px 10px; margin: 0px 20px; border-radius: 10px;}""")

            self.label2 = QLabel()
            self.label2.setVisible(False)
            self.label2.setMaximumSize(600,30)
            self.label2.setStyleSheet("""QLabel {background-color:pink; padding:5px 10px; margin: 0px 20px; border-radius: 10px;}""")

            self.le_link = QLineEdit()
            self.le_link.setClearButtonEnabled(True)
            self.le_link.setStyleSheet("QLineEdit {background-color:pink; padding:5px 10px; margin: 0px 20px; border-radius: 5px}")
            self.le_link.setMinimumSize(300,30)
            self.le_link.setPlaceholderText("Video linki veya Oynatma Listesi linki")

            self.btn_video = QPushButton("Video indir", self)
            self.btn_video.setStyleSheet("""QPushButton {background-color:pink; border-radius: 5px}
                                            QPushButton:hover {background-color: #edb4da;}""")
            self.btn_video.setMaximumSize(100,30)
            self.btn_video.clicked.connect(downloadWithTread)

            self.btn_mp3 = QPushButton("mp3 indir", self)
            self.btn_mp3.setStyleSheet("""QPushButton {background-color:pink; border-radius: 5px;}
                                          QPushButton:hover {background-color: #edb4da;  }""")
            self.btn_mp3.setMaximumSize(100, 30)
            self.btn_mp3.clicked.connect(downloadWithTread)

            self.progress = QProgressBar(self)
            self.progress.setMaximumSize(600,20)
            self.progress.setStyleSheet("""QProgressBar {background-color:white; border: 2px solid gray; border-radius: 5px; padding:1px 3px; margin: 0px 20px; font-size:8}""")
            self.progress.setValue(0)
            self.progress.setVisible(False)

            vlayout.addWidget(self.label)
            vlayout.addWidget(self.le_link)
            hlayout.addWidget(self.btn_mp3)
            hlayout.addWidget(self.btn_video)
            vlayout.addLayout(hlayout)
            vlayout.addWidget(self.progress)
            vlayout.addWidget(self.label2)

            self.widget = QWidget()
            self.setCentralWidget(self.widget)
            self.widget.setLayout(vlayout)
        except Exception as E:
            print(E)



    def getDownloadLinks(self) -> list :
        try:
            link = self.le_link.text()
            if "watch" in link:
                return [link,]
            elif "playlist" in link:
                pl = Playlist(link)
                return pl
            return None
        except Exception as E:
            print(E)

    def download(self):
        try:
            sender = self.sender().text()
            linkListesi = self.getDownloadLinks()
            print(linkListesi)
            if linkListesi:
                work, count = len(linkListesi), 0
                self.progress.setMaximum(work)
                self.progress.setVisible(True)
                self.progress.setValue(0)
                self.statusbar.clearMessage()
                for link in linkListesi:
                    yt = YouTube(link)
                    self.label2.setVisible(True)
                    self.label2.setText(f"'{yt.title}' indiriliyor...")
                    strim = yt.streams
                    if sender == "mp3 indir":
                        output = strim.filter(type="audio", abr="128kbps")[0].download(output_path="Download Music")
                        base, ext = os.path.splitext(output)
                        to_mp3 = base + ".mp3"
                        os.rename(output, to_mp3)
                    elif sender == "Video indir":
                        strim.get_highest_resolution().download(output_path="Download Video")
                    count +=1
                    self.progress.setValue(count)
                    self.statusbar.showMessage(f"{count}/{work} indirme devam ediyor...")
                self.statusbar.showMessage(f"{count}/{work} indirme yapıldı. İşlem tamamlandı.")
                self.label2.setVisible(False)
        except Exception as E:
            self.statusbar.showMessage(f"Geçersiz bir link girdiniz !!!", 10000)
            print(E)

def main():
    global win
    try:
        app = QApplication(sys.argv)
        font = QtGui.QFont()
        font.setBold(True)
        font.setFamilies(["Arial"])
        font.setPointSize(11)
        app.setFont(font)
        win = YoutubeDown()
        win.show()
        sys.exit(app.exec_())
    except Exception as E:
        print(E)

if __name__ == '__main__':
    main()


#------------------- pyinstaller --noconsole --onefile -i "youtube.ico" main.py ------------------#