'''
Basic tests for the file renaming functions.
'''
from codeforgoof.file_io import FileRenamer
from pathlib import Path
import tempfile

def create_test_files(base_dir: Path, filenames: list[str]) -> None:
    for filename in filenames:
        file_path = base_dir / filename
        file_path.touch()

def test_iteratively_replace_file_name() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        # Also test with subdirectories
        
        
        test_filenames = ["file one.txt", "file two.txt", "another file.txt"]
        create_test_files(base_path, test_filenames)
        
        renamer = FileRenamer(base_path, old_str=" ", new_str="_")
        renamer.rename_files()
        
        expected_filenames = ["file_one.txt", "file_two.txt", "another_file.txt"]
        for filename in expected_filenames:
            assert (base_path / filename).exists()
        
        for filename in test_filenames:
            assert not (base_path / filename).exists()

        # Now test undo
        renamer.undo_rename()
        for filename in test_filenames:
            assert (base_path / filename).exists()
            