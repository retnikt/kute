from PyQt5 import QtWidgets


class KuteMainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.v_layout)
        self.v_layout.addLayout(self.h_layout)
        self.widgets = Namespace()
        self.ui()

    def ui(self):
        status_bar = self.statusBar()
        status_bar.showMessage("Test 123")

        editor = QtWidgets.QTextEdit()

        # Menu bar
        menu_bar = QtWidgets.QMenuBar(self)
        for title, items in self.menus.items():
            menu = menu_bar.addMenu(title)
            for i in items:
                action = QtWidgets.QAction(i, self)
                action.triggered.connect(factory(i))
                menu.addAction(action)
        self.setMenuBar(menu_bar)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = KuteMainWindow()
    window.show()
    sys.exit(app.exec_())
