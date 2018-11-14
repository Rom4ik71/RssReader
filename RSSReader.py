# сайты для парсинга брал https://subscribe.ru/catalog?rss

# Примеры сайтов:
#http://feeds.feedburner.com/apple/SVwD
#http://echo.msk.ru/news.rss
#http://feeds.feedburner.com/yandex/MAOo


# #Rss reader ptrototype

#Реализовано только чтение и визуализация, является прототипом
import feedparser
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from PyQt5.QtWidgets import QFrame, QPushButton, QTableView, QAbstractItemView, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, QUrl, QVariant, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class RssModel(QAbstractTableModel):

    def __init__(self, datain, parent=None):
        #Иницилизируем Rss class
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain

    def rowCount(self, parent):
        #Возвращает количество столбцов в arraydata
        return len(self.arraydata)

    def columnCount(self, parent):
        #возвращает количество колонок в arraydata
        if len(self.arraydata) > 0:
            return len(self.arraydata[0]) - 2
        return 0

    def data(self, index, role=Qt.DisplayRole):
        #функция возвращает значения для первой и второй колонки, то есть будет изображен Title & Website
        if not index.isValid():
            return QVariant()
        elif index.column() < 2:
            if role == Qt.DisplayRole:
                return QVariant(self.arraydata[index.row()][index.column()])
            return QVariant()
        return QVariant()

    def update(self, datain):
        self.arraydata = datain
        self.layoutChanged.emit()

    def summary(self, index):
        return self.arraydata[index.row()][2]

    def url(self, index):
        return self.arraydata[index.row()][3]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Title", "Website"][section]
            if orientation == Qt.Vertical:
                return None


class RssFrame(QFrame,QtWidgets.QPushButton,QtWidgets.QWidget):

    def __init__(self, parent=None):
        #класс RssFrame
        
        super().__init__()
    #заставка
    def load_data(self,sp):
        for i in range(1,100):
            time.sleep(0.05)
            sp.showMessage("Загрузка данных... {0}%".format(i+1),
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop, QtCore.Qt.white)

            QtWidgets.qApp.processEvents()


        self.data = []

        self.resize(1280, 720)
        self.setWindowTitle('RSS Reader beta v1.0.1')

        
        #наначение обработчиков сигнала

        self.button1 = QPushButton()
        self.button1.setText("Получить новости")
        self.button1.clicked.connect(self.on_clicked_button1)
        self.button1.clicked.connect(self.addurl)
        self.button1.setCursor(QtCore.Qt.ClosedHandCursor)

        self.button2 = QPushButton("Удалить новости")
        self.button2.clicked.connect(self.on_clicked_button2)
        self.button2.setCursor(QtCore.Qt.ClosedHandCursor)

        #self.button1.setCursor(QtCore.Qt.ClosedHandCursor)

        self.rssTable = QTableView()
        self.rssTable.clicked.connect(self.on_click)
        self.rssTable.doubleClicked.connect(self.on_double_click)
        self.rssTable.setCursor(QtCore.Qt.CrossCursor)

        self.rssModel = RssModel(self.data)
        self.rssTable.setModel(self.rssModel)
        self.rssTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.header = self.rssTable.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)


        feedURL = QLabel()
        feedURL.setText("<FONT COLOR=white face=Courier New>Вставьте URL:</FONT>")
        self.feedURLEdit = QLineEdit()
        self.listURL = QtWidgets.QComboBox()
        self.listURL.addItem("http://feeds.feedburner.com/apple/SVwD")
        self.listURL.addItem("http://echo.msk.ru/news.rss")
        self.listURL.addItem("http://feeds.feedburner.com/yandex/MAOo")
        self.listURL.activated.connect(self.onclick_URL)


        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        

        self.searcher = QLineEdit()
        self.searcher.textChanged.connect(self.search_words)
         
        self.sortFilter = QtCore.QSortFilterProxyModel()
        self.sortFilter.setSourceModel(self.rssModel)
        self.sortFilter.setFilterKeyColumn(0)


        self.rssTable.setModel(self.sortFilter)

        #хотелось бы сделать обработку, если человек не ввел текст, то он не должен нажимать кнопку "получить новость"
        #примерно так
        # if len(QlineEdit) == 0:
        #   self.button1.setCursor(QtCore.Qt.ClosedHandCursor)


        self.description = QTextEdit()
        self.description.setReadOnly(True)

        #Компоненты-контейнеры

        grid = QGridLayout() #Создаём сетку  
        grid.setSpacing(9)

        sublayout = QHBoxLayout() #выстраивает все комоненты по горизонтали
        sublayout.addWidget(feedURL)
        sublayout.addWidget(self.feedURLEdit)
        #sublayout.addWidget(self.searcher)
        sublayout.addWidget(self.listURL)
        sublayout.addWidget(self.button1)
        sublayout.addWidget(self.button2)
        
        
        grid.addLayout(sublayout, 0, 0, 1, 2)
        #grid.addWidget(self.feedURL, 0, 0)
        grid.addWidget(self.searcher, 1, 0, 1, 1)
        grid.addWidget(self.rssTable, 2, 0, 1, 1)
        grid.addWidget(self.description, 3, 0, 1, 1)
        grid.addWidget(self.browser, 1 , 1 , 3, 1 )

        
        self.setLayout(grid) #передаем ссылку родителям

        self.show()

    #классы PyQt5 поддерживают ряд методов, специально предназначенных в качестве обработчиков синалов. Такие методы называются слотами!
    #Любой пользовательский метод можно сделать слотом, для чего необходимо перед ео определением вставить декоратор @pyqtSlot()
    #Формат декоратора



    @pyqtSlot()
    def on_clicked_button1(self):
        #при нажатии кнопки вызывается функция, которая парсит rss-chanel на новости
        if self.feedURLEdit.text() !=0:
            rss = self.feedURLEdit.text()
            feed = feedparser.parse(str(rss))
            website = feed["feed"]["title"]
            for key in feed["entries"]:
                title = key["title"]
                link = key["link"]
                summary = key["summary"]
                self.data.append([title, website, summary, link])
            self.rssModel.update(self.data)
            self.rssTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.feedURLEdit.clear()
    @pyqtSlot()
    def on_clicked_button2(self):
        #при нажатии кнопки вызывается функция, которая парсит rss-chanel на новости
        rss = self.feedURLEdit.text()
        feed = feedparser.parse(str(rss))

        website = feed["feed"]["title"]
        for key in feed["entries"]:
            title = key["title"]
            link = key["link"]
            summary = key["summary"]
            self.data.remove([title, website, summary, link])

        self.rssModel.update(self.data)
        self.description.clear()
        self.browser.clearMask()
        
    @pyqtSlot()
    def onclick_URL(self):
        self.feedURLEdit.clear()
        a = self.listURL.currentText()
        self.feedURLEdit.insert(a)


    @pyqtSlot()
    def on_click(self):
        #извлекается индес полученной rssTable, используемый для получения сводки выбранной записи, которая завернута в html-теги
        index = self.rssTable.selectedIndexes()[0]
        html = "<html><body>%s</body></html>" % self.rssModel.summary(index)
        self.description.setHtml(html)

    @pyqtSlot()
    def on_double_click(self):
       #двойное нажатие привёдет к отображению сайта в правой части экрана с помощью модуля QtWebEngineView
        index = self.rssTable.selectedIndexes()[0]
        url = QUrl(self.rssModel.url(index))
        self.browser.load(url)
        self.browser.show()

    @pyqtSlot()
    def search_words(self):
        self.sortFilter.setFilterWildcard(self.searcher.text())

    @pyqtSlot()
    def addurl(self):
        if (self.listURL.findText(self.feedURLEdit.text())) == -1:
            self.listURL.addItem(self.feedURLEdit.text())  


    
    def closeEvent(self, e):
        #закрытие окна
        result = QtWidgets.QMessageBox.question(self,"Подтверждение закрытия окна", "Вы действительно хотите закрыть окно?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self,e)
        else:
            e.ignore()
    
    

if __name__ == '__main__':

    import sys


    app = QtWidgets.QApplication(sys.argv)
    frame = RssFrame()

    ico = QtGui.QIcon("1.png")
    frame.setWindowIcon(ico)
    app.setWindowIcon(ico)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("1.png"))
    splash.showMessage("Загрузка данных... 0%",
    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop, QtCore.Qt.white)
    splash.show()
    QtWidgets.qApp.processEvents()
    frame.load_data(splash)

    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() - frame.width()) // 2
    y = (desktop.height() - frame.height()) // 2
    frame.move(x,y)
    
    frame.setWindowOpacity(0.98)

    #pal = frame.palette()
    #pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor("#dfd3cd"))
    #pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor("#dfd3cd"))
    #frame.setPalette(pal)

    pal = frame.palette()
    pal.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QBrush(QtGui.QPixmap("c13.jpg")))
    pal.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QBrush(QtGui.QPixmap("c13.jpg")))
    frame.setPalette(pal)

    frame.show()
    splash.finish(frame)




    
    
    
    sys.exit(app.exec_())
