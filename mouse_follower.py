import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import QCursor #want know mouse position
#want know mouse position


class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0, 0]
        self.to_xy = xy
        self.to_xy_diff = [0, 0]
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None

        self.setupUi()
        self.show()
    def move(self, x, y):
        self.xy = [x, y]
        super(Sticker, self).move(x, y)
    
    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        #give flag for alaways select
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        #.X11BypassWindowManagerHint is for alaways select
        
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.WA_ShowWithoutActivating|
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint| QtCore.Qt.X11BypassWindowManagerHint|QtCore.Qt.WindowSystemMenuHint if self.on_top else QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.Tool)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        self.setGeometry(self.xy[0], self.xy[1], w, h) #setgeometry is the size of the window
        self.move(self.xy[0], self.xy[1]) #move is the position of the window
        self.timer.timeout.connect(self.find_cusor)
        self.timer.start(5)
    def find_cusor(self):
        self.localPos = QCursor.pos()
        self.move(self.localPos.x()-100, self.localPos.y()+-100)
        #pess ~ to quit
        if self.localPos.x() == 0 and self.localPos.y() == 0:
            self.close()
            sys.exit()

app = QtWidgets.QApplication(sys.argv)
s = Sticker('c:/hm/test.gif', xy=[-80, 200], on_top=False)
sys.exit(app.exec_())