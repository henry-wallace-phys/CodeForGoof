import sys

from PyQt5.QtWidgets import QApplication

from codeforgoof.file_io import FileRenamer
from codeforgoof.pyqt.pyqt_browsers import FolderActionMenu


def rename_action(selected_folder: str, renamer: FileRenamer):
    renamer.rename_files(selected_folder)


def undo_rename_action(renamer: FileRenamer):
    renamer.undo_rename()


def pyqt_file_renamer():
    renamer = FileRenamer()

    def action_callback(selected_folder: str):
        rename_action(selected_folder, renamer)

    def undo_callback():
        undo_rename_action(renamer)

    app = QApplication(sys.argv)

    menu = FolderActionMenu(
        action_callback=action_callback,
        undo_callback=undo_callback,
        title="File Renamer Menu",
        action_name="Rename Files",
    )
    menu.show()

    sys.exit(app.exec_())
