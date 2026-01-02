"""
Generic PyQt file browser and window to open folder browser.
Additional functionality can be added.
"""

import sys
from collections.abc import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GenericFolderSelector:
    def __init__(self, title: str = "Select Folder", initial_dir: str = "/"):
        self.title = title
        self.initial_dir = initial_dir

    def browse_folder(self) -> str | None:
        folder_path = QFileDialog.getExistingDirectory(
            None,
            self.title,
            self.initial_dir,
            QFileDialog.ShowDirsOnly,
        )
        return folder_path if folder_path else None


class FolderActionMenu(QWidget):
    """
    Menu for:
    | Select folder: <Browse Button> | Display selected folder path
    | Perform Action Button | Undo Action Button | Quit Button |

    Undo is disabled until an action is performed.
    """

    def __init__(
        self,
        action_callback: Callable[[str], None],
        undo_callback: Callable[[], None],
        title: str = "Folder Action Menu",
        action_name: str = "Perform Action",
    ):
        super().__init__()

        self.action_callback = action_callback
        self.undo_callback = undo_callback
        self.selected_folder: str | None = None
        self.action_performed = False
        self.action_name = action_name

        self.setWindowTitle(title)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        self.folder_label = QLabel("No folder selected")
        self.folder_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.folder_label)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.action_button = QPushButton(f"{self.action_name}")
        self.action_button.clicked.connect(self.perform_action)
        self.action_button.setEnabled(False)
        layout.addWidget(self.action_button)

        self.undo_button = QPushButton("Undo Action")
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.undo_action)
        layout.addWidget(self.undo_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(QApplication.quit)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

    def browse_folder(self):
        folder_selector = GenericFolderSelector()
        folder_path = folder_selector.browse_folder()

        if folder_path:
            self.selected_folder = folder_path
            self.folder_label.setText(f"Selected Folder:\n{folder_path}")
            self.action_button.setEnabled(True)

    def perform_action(self):
        if self.selected_folder:
            self.action_callback(self.selected_folder)
            self.action_performed = True
            self.undo_button.setEnabled(True)

    def undo_action(self):
        if self.action_performed:
            self.undo_callback()
            self.action_performed = False
            self.undo_button.setEnabled(False)


# Example usage
if __name__ == "__main__":
    def example_action(folder: str):
        print(f"Action performed on: {folder}")

    def example_undo():
        print("Action undone")

    app = QApplication(sys.argv)
    window = FolderActionMenu(example_action, example_undo)
    window.show()
    sys.exit(app.exec_())
