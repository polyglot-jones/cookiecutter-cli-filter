from PyQt5 import uic
from pathlib import Path
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow
import logging

LOG = logging.getLogger("main")


(DialogSpec, BaseClass) = uic.loadUiType("{{ cookiecutter.tool_name_slug }}\\gui\\editor.ui", from_imports=True, import_from="{{ cookiecutter.tool_name_slug }}.gui")


class {{ cookiecutter.tool_name_slug }}Window(BaseClass, DialogSpec):
    """
    Main window for the desktop app.
    """

    def __init__(self, parent, switches, config):
        LOG.trace("Enter: {{ cookiecutter.tool_name_slug }}Window __init__")
        BaseClass.__init__(self)
        DialogSpec.__init__(self)
        self.parent = parent
        global SWITCHES, CONFIG
        SWITCHES = switches
        CONFIG = config
        self.setupUi(self)

        self.setWindowIcon(QIcon('{{ cookiecutter.tool_name_slug }}/assets/{{ cookiecutter.tool_name_slug }}_icon.png'))

        self.connect_actions()
        self.statusBar()


    def file_open(self):
        name,_ = QFileDialog.getOpenFileName(self, 'Open File', directory=CONFIG.dataDir)
        path = Path(name)
        with path.open("rt") as input_file:
            # TODO Use input_file here

    def file_save(self):
        name,_ = QFileDialog.getSaveFileName(self, 'Save File')
        path = Path(name)
        with path.open("wt") as output_file:
            # TODO output_file.write(???)

    def print(self):
        pass

    def page_setup(self):
        pass

    def connect_actions(self):
        # self.action_About.triggered.connect(self.)
        # self.action_AsciiDoc_View.triggered.connect(self.)
        # self.action_Bug.triggered.connect(self.)
        self.action_Close.triggered.connect(self.close_application)
        # self.action_Copy.triggered.connect(self.)
        # self.action_Cut.triggered.connect(self.)
        # self.action_Distraction_Free.triggered.connect(self.)
        # self.action_Exit.triggered.connect(self.)
        # self.action_Find.triggered.connect(self.)
        self.action_Font.triggered.connect(self.font_choice)
        # self.action_Help.triggered.connect(self.)
        # self.action_New.triggered.connect(self.)
        self.action_Open.triggered.connect(self.file_open)
        # self.action_Paste.triggered.connect(self.)
        self.action_Print.triggered.connect(self.print)
        # self.action_Print_Preview.triggered.connect(self.preview)
        # self.action_Redo.triggered.connect(self.)
        self.action_Save.triggered.connect(self.file_save)
        self.action_Save_As.triggered.connect(self.file_save)
        # self.action_Select_All.triggered.connect(self.)
        # self.action_Undo.triggered.connect(self.)
        # self.action_Updates.triggered.connect(self.)
        # self.action_Wrap_Text.triggered.connect(self.)


    def close_application(self):
        self.close()


