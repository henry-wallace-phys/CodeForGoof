"""
Generic PyQt file browser and window to open folder browser.
Additional functionality can be added.
"""

import sys
from collections.abc import Callable
from io import StringIO

from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class OutputRedirector(QObject):
    """Redirects stdout to a Qt signal for display in GUI."""
    output_written = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.buffer = StringIO()

    def write(self, text):
        if text and text != '\n':
            self.output_written.emit(text)
        # Also write to original stdout for debugging if needed
        sys.__stdout__.write(text)

    def flush(self):
        pass


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
    | Output Panel (shows print statements and program output) |

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
        
        # Set up output redirection
        self.output_redirector = OutputRedirector()
        self.output_redirector.output_written.connect(self.append_output)
        sys.stdout = self.output_redirector
        
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        # Create a splitter to allow resizing between controls and output
        splitter = QSplitter(Qt.Vertical)

        # Top widget with controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout()

        self.folder_label = QLabel("No folder selected")
        self.folder_label.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(self.folder_label)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        controls_layout.addWidget(self.browse_button)

        self.action_button = QPushButton(f"{self.action_name}")
        self.action_button.clicked.connect(self.perform_action)
        self.action_button.setEnabled(False)
        controls_layout.addWidget(self.action_button)

        self.undo_button = QPushButton("Undo Action")
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.undo_action)
        controls_layout.addWidget(self.undo_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit_application)
        controls_layout.addWidget(self.quit_button)

        controls_widget.setLayout(controls_layout)

        # Output panel widget
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        
        output_label = QLabel("Output:")
        output_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Program output will appear here...")
        output_layout.addWidget(self.output_text)
        
        # Clear output button
        self.clear_button = QPushButton("Clear Output")
        self.clear_button.clicked.connect(self.clear_output)
        output_layout.addWidget(self.clear_button)
        
        output_widget.setLayout(output_layout)

        # Add widgets to splitter
        splitter.addWidget(controls_widget)
        splitter.addWidget(output_widget)
        
        # Set initial sizes (controls get 40%, output gets 60%)
        splitter.setSizes([300, 400])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
        # Set minimum window size
        self.setMinimumSize(500, 600)

    def append_output(self, text: str):
        """Append text to the output panel."""
        self.output_text.append(text.rstrip())
        # Auto-scroll to bottom
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )

    def clear_output(self):
        """Clear the output panel."""
        self.output_text.clear()

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

    def quit_application(self):
        """Restore stdout before quitting."""
        sys.stdout = sys.__stdout__
        QApplication.quit()

    def closeEvent(self, event):
        """Restore stdout when window is closed."""
        sys.stdout = sys.__stdout__
        event.accept()


# Example usage
if __name__ == "__main__":
    def example_action(folder: str):
        print(f"Action performed on: {folder}")
        print("This is additional output that will appear in the panel")
        for i in range(5):
            print(f"Processing step {i+1}...")

    def example_undo():
        print("Action undone")
        print("All changes have been reverted")

    app = QApplication(sys.argv)
    window = FolderActionMenu(example_action, example_undo)
    window.show()
    sys.exit(app.exec_())