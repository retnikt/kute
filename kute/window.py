from PyQt5 import QtWidgets, QtGui, QtCore
import syntax
#from .


class KuteWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace = KuteWorkspaceFrame(None, self)
        self.setCentralWidget(self.workspace)


class KuteWorkspaceFrame(QtWidgets.QFrame):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.v_layout)
        self.ui()

    def ui(self):
        editor = QtWidgets.QTextEdit(self)
        syntax.PythonSyntaxHighlighter(syntax.SyntaxHighlightStyles(), editor.document())
        self.v_layout.addWidget(editor, 1)

    @classmethod
    def from_config(cls, config):
        return cls(config)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = KuteWindow()
    pal = QtGui.QPalette()
    pal.setColor(QtGui.QPalette.Background, QtGui.QColor("red"))
    # window.workspace.setPalette(pal)
    window.show()
    sys.exit(app.exec_())
