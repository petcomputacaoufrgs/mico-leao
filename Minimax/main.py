import sys
import gui
from PySide6 import QtWidgets


if __name__ == "__main__":
   app = QtWidgets.QApplication([])

   game = gui.MainWindow()
   game.launch()
   game.resize(800, 600)
   game.show()

   sys.exit(app.exec())
