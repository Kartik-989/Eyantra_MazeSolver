

'''

eYRC 2019-20 - Rapid Rescuer (RR)
RR_start_screen.py

'''


# import libraries
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from global_variables import Global_Vars
import subprocess

# create object for Global_Vars class
global_vars = Global_Vars()

# enter UI file here
qtCreatorFile = "RR_eYRC_2019-20_start_screen.ui"

# load the UI MainWindow and Base Class of Qt from UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# global variables
Team_ID = 0

# to translate plainText to HTML script
_translate = QtCore.QCoreApplication.translate


class Start_Screen_App(QtWidgets.QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)

		self.setupUi(self)
		
		self.setWindowTitle("eYRC 2019-20: Rapid Rescuer (RR)")
		
		# find the size of the 'central_widget'
		gui_width, gui_height = self.frameGeometry().width(), self.frameGeometry().height()

		# set the size and position of 'gui_title_label'
		gui_title_width, gui_title_height = self.gui_title_label.frameGeometry().width(), self.gui_title_label.frameGeometry().height()
		self.gui_title_label.setGeometry(QtCore.QRect((gui_width - gui_title_width)/2, self.gui_title_label.frameGeometry().y(), \
														gui_title_width, gui_title_height))

		self.next_button.clicked.connect(self.Next_GUI)

		self.exit_button.clicked.connect(self.Exit_GUI)
	
		

	def Next_GUI(self):
		
		global Team_ID

		Team_ID = int(self.team_id.toPlainText())

		subprocess.call(["python3", "layout_logic.pyc", "--team_id", str(Team_ID)])

		sys.exit()

	

	def Exit_GUI(self):
		
		sys.exit()



if __name__ == "__main__":
	
	start_screen_app = QtWidgets.QApplication(sys.argv)

	screen_resolution = start_screen_app.desktop().screenGeometry()
	screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

	window = Start_Screen_App()
	window.show()

	sys.exit(start_screen_app.exec_())




