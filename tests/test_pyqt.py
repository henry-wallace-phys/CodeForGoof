"""
GUI tests for pyqt_file_renamer using pytest-qt
"""

import sys

import pytest
from PyQt5.QtWidgets import QApplication

from codeforgoof.pyqt.pyqt_browsers import FolderActionMenu


@pytest.fixture(scope="session")
def app():
    """Ensure a single QApplication exists"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def test_menu_initial_state(app, qtbot):
    called_action = False
    called_undo = False

    def action_callback(folder):
        nonlocal called_action
        called_action = True

    def undo_callback():
        nonlocal called_undo
        called_undo = True

    menu = FolderActionMenu(action_callback, undo_callback)
    qtbot.addWidget(menu)

    assert menu.folder_label.text() == "No folder selected"
    assert not menu.undo_button.isEnabled()

def test_folder_selection_updates_label(app, qtbot, tmp_path):
    selected_folder = tmp_path

    def dummy_action(folder):
        pass

    def dummy_undo():
        pass

    menu = FolderActionMenu(dummy_action, dummy_undo)
    qtbot.addWidget(menu)

    # Simulate selecting a folder
    menu.selected_folder = selected_folder
    menu.folder_label.setText(f"Selected Folder:\n{selected_folder}")

    assert menu.selected_folder == selected_folder
    assert menu.folder_label.text() == f"Selected Folder:\n{selected_folder}"

def test_perform_action_triggers_callback_and_enables_undo(app, qtbot, tmp_path):
    action_called = False
    undo_called = False

    def action_callback(folder):
        nonlocal action_called
        action_called = True

    def undo_callback():
        nonlocal undo_called
        undo_called = True

    menu = FolderActionMenu(action_callback, undo_callback)
    qtbot.addWidget(menu)

    # Simulate selecting a folder
    menu.selected_folder = tmp_path

    menu.perform_action()

    assert action_called
    assert menu.undo_button.isEnabled()
    assert menu.action_performed

def test_undo_action_triggers_callback_and_disables_button(app, qtbot, tmp_path):
    undo_called = False

    def action_callback(folder):
        pass

    def undo_callback():
        nonlocal undo_called
        undo_called = True

    menu = FolderActionMenu(action_callback, undo_callback)
    qtbot.addWidget(menu)

    # Simulate a performed action
    menu.selected_folder = tmp_path
    menu.action_performed = True
    menu.undo_button.setEnabled(True)

    menu.undo_action()

    assert undo_called
    assert not menu.undo_button.isEnabled()
    assert not menu.action_performed
