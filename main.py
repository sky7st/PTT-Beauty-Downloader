from PyQt4 import QtGui,QtCore
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str
import sys,os,webbrowser,queue,time
import beautyUi,aboutAppUi,beauty

class TestApp(QtGui.QMainWindow, beautyUi.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__();
        self.setupUi(self)
        self.connect(self.goToBeauty, QtCore.SIGNAL('aboutToShow()'),lambda:webbrowser.open('https://www.ptt.cc/bbs/beauty/index.html'))
        
        self.connect(self.choosePathButton, QtCore.SIGNAL('clicked()'), self.pick_new)
        self.defaultDownloadPath = os.getcwd() + "\Download"
        self.DownloadPath = self.defaultDownloadPath
        self.choosePathLabel.setText(self.DownloadPath)
        
        self.allPageNum = int(beauty.get_all_page())
        self.allPageNumLabel.setText(str(self.allPageNum))

        
        self.firstPageChooseNum = 0
        self.finalPageChooseNum = 0
        self.pageQueue = queue.Queue()

        self.connect(self.sendPageButton, QtCore.SIGNAL('clicked()'), self.parse_pages)
        self.articleQueue = queue.Queue()
        self.articleNum = 0

        self.tellTitleNumLabel.hide()
        self.downloadButton.hide()

        self.connect(self.openFolder, QtCore.SIGNAL('clicked()'), self.open_folder)
        self.connect(self.QuitButton,QtCore.SIGNAL('clicked()'), QtGui.qApp.quit)
        
        
    def pick_new(self):
        dialog = QtGui.QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "選擇資料夾")
        if folder_path == "":
            self.DownloadPath = self.defaultDownloadPath
        else:
            self.DownloadPath = folder_path
        self.choosePathLabel.setText(self.DownloadPath)
    
    def open_folder(self):
        command = 'explorer.exe "'+ self.DownloadPath + '"'
        print(command)
        os.system(command)
    
    def parse_pages(self):
        if self.pageQueue.qsize() > 0:
            self.pageQueue.queue.clear()
        if self.articleQueue.qsize() > 0:
            self.articleQueue.queue.clear()
        self.sendPageButton.setText("解析中")
        self.sendPageButton.setEnabled(False)
        self.stopSend.setEnabled(True)
        firstText = self.firstPageTextedit.text()
        finalText = self.finalPageTextedit.text()
        threadList = []
        if not firstText.isdigit() or not finalText.isdigit(): 
            QtGui.QMessageBox.critical(self, "錯誤", "請輸入數字!", QtGui.QMessageBox.Cancel)
            self.articleQueue = None
            return
        elif int(finalText) < int(firstText) :
            self.firstPageChooseNum = int(finalText)
            self.finalPageChooseNum = int(firstText)
        else:
            self.firstPageChooseNum = int(firstText)
            self.finalPageChooseNum = int(finalText)
        allNum =self.finalPageChooseNum - self.firstPageChooseNum + 1
        for i in range(self.firstPageChooseNum,self.finalPageChooseNum+1):
            self.pageQueue.put(i)

        for j in range(8):
            pageThread = Worker(i, "getArticle", self.pageQueue,self.articleQueue, allPageNum=self.allPageNum)
            threadList.append(pageThread)
        while(not self.pageQueue.empty()):
            for thread in threadList:
                thread.start()
                QtCore.QCoreApplication.processEvents()
                nowNum = allNum - self.pageQueue.qsize()
                downloadPar = int((float(nowNum)/allNum)*100)
                self.downloadBar.setValue(downloadPar)
                # thread.wait()
        self.downloadBar.setValue(100)
        self.sendPageButton.setEnabled(True)
        self.stopSend.setEnabled(False)
        time.sleep(1)
        self.articleNum = self.articleQueue.qsize()
        self.sendPageButton.setText("解析")
        print("end")
                        



class Worker(QtCore.QThread):
    def __init__(self, threadId, name, pageQueue, articleQueue, parent=None, allPageNum=None):
        super().__init__(parent)
        self.threadId = threadId
        self.pageQueue = pageQueue 
        self.articleQueue = articleQueue
        self.name = name 
        self.allPageNum = allPageNum    
    def run(self): 
        if "getArticle" in self.name:
            # while(not self.queue.empty()):
                pageNum = self.pageQueue.get()
                articleList = beauty.get_page_article(self.allPageNum,pageNum)
                for article in articleList:
                    print(article)
                    self.articleQueue.put(article)
                print("end parse\n")
 
def main():
    app = QtGui.QApplication(sys.argv)
    form = TestApp()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()