'''
Basic tests for the file renaming functions.
'''
from codeforgoof.file_io import iteratively_replace_file_name, rename_stuff
from pathlib import Path
import tempfile
import os
import shutil
import pytest

def create_test_files(base_dir: Path, filenames: list[str]) -> None:
    for filename in filenames:
        file_path = base_dir / filename
        file_path.touch()

def test_iteratively_replace_file_name() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        test_filenames = ["file one.txt", "file two.txt", "another file.txt"]
        create_test_files(base_path, test_filenames)
        
        iteratively_replace_file_name(base_path, old_str=" ", new_str="_")
        
        expected_filenames = ["file_one.txt", "file_two.txt", "another_file.txt"]
        for filename in expected_filenames:
            assert (base_path / filename).exists()
        
        for filename in test_filenames:
            assert not (base_path / filename).exists()
