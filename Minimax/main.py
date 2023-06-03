import sys
import gui
import qdarkstyle
from PySide6 import QtWidgets


if __name__ == "__main__":
   app = QtWidgets.QApplication([])
   dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
   app.setStyleSheet(dark_stylesheet)

   game = gui.MainWindow()
   game.launch()
   game.resize(800, 600)
   game.show()

   sys.exit(app.exec())
