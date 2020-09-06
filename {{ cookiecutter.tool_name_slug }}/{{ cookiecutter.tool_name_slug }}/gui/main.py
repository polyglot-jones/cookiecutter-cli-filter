import argparse
import subprocess
import sys
import logging
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow
from gwpycore import ICON_INFO, inform_user_about_issue
import {{ cookiecutter.tool_name_slug }}.gui.main_ui_rc

LOG = logging.getLogger("main")
CONFIG: argparse.Namespace

BUG_REPORT_URL = "https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.github_repo }}/issues/"
HELP_URL = "https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.github_repo }}"

(DialogSpec, BaseClass) = uic.loadUiType("{{ cookiecutter.tool_name_slug }}\\gui\\main.ui", from_imports=True, import_from="{{ cookiecutter.tool_name_slug }}.gui")


class {{ cookiecutter.tool_name_slug }}Window(BaseClass, DialogSpec):
    """
    Main window for the desktop app.
    """

    def __init__(self, parent, config):
        LOG.trace("Enter: {{ cookiecutter.tool_name_slug }}Window __init__")
        BaseClass.__init__(self)
        DialogSpec.__init__(self)
        self.parent = parent
        global CONFIG
        CONFIG = config
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/main_ui/{{ cookiecutter.tool_name_slug }}_icon.ico'))

        self.connect_actions()
        self.statusBar()


    def about(self):
        inform_user_about_issue(message=f"{{ cookiecutter.tool_name }}\nVersion {CONFIG.version}", icon = ICON_INFO, title="About", parent=self)

    def bug(self):
        subprocess.run(['open', BUG_REPORT_URL], check=True)

    def copy(self):
        pass

    def cut(self):
        pass

    def full_screen(self):
        pass

    def file_close(self):
        pass

    def file_new(self):
        pass

    def file_open(self):
        name,_ = QFileDialog.getOpenFileName(self, 'Open File', directory=CONFIG.dataDir)
        path = Path(name)
        with path.open("rt") as input_file:
            # TODO Use input_file here
            pass

    def file_save(self):
        name,_ = QFileDialog.getSaveFileName(self, 'Save File')
        path = Path(name)
        with path.open("wt") as output_file:
            # TODO output_file.write(???)
            pass

    def file_save_as(self):
        pass

    def find(self):
        pass

    def font_choice(self):
        pass

    def help(self):
        subprocess.run(['open', HELP_URL], check=True)

    def paste(self):
        pass

    def preview(self):
        pass

    def print(self):
        pass

    def redo(self):
        pass

    def select_all(self):
        pass

    def undo(self):
        pass

    def updates(self):
        pass

    def wrap_text(self):
        pass

    def connect_actions(self):
        self.action_About.triggered.connect(self.about)
        self.action_Bug.triggered.connect(self.bug)
        self.action_Close.triggered.connect(self.file_close)
        self.action_Exit.triggered.connect(self.close_application)
        self.action_Copy.triggered.connect(self.copy)
        self.action_Cut.triggered.connect(self.cut)
        self.action_Full_Screen.triggered.connect(self.full_screen)
        self.action_Find.triggered.connect(self.find)
        self.action_Font.triggered.connect(self.font_choice)
        self.action_Help.triggered.connect(self.help)
        self.action_New.triggered.connect(self.file_new)
        self.action_Open.triggered.connect(self.file_open)
        self.action_Paste.triggered.connect(self.paste)
        self.action_Print.triggered.connect(self.print)
        self.action_Print_Preview.triggered.connect(self.preview)
        self.action_Redo.triggered.connect(self.redo)
        self.action_Save.triggered.connect(self.file_save)
        self.action_Save_As.triggered.connect(self.file_save_as)
        self.action_Select_All.triggered.connect(self.select_all)
        self.action_Undo.triggered.connect(self.undo)
        self.action_Updates.triggered.connect(self.updates)
        self.action_Wrap_Text.triggered.connect(self.wrap_text)


    def close_application(self):
        self.close()

