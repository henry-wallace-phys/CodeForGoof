from pathlib import Path
from tqdm import tqdm
from typing import Optional


class FileRenamer:
    def __init__(self, directory: Optional[Path | str]=None, old_str: str=" ", new_str: str="_") -> None:
        """
        Initializes the FileRenamer with the specified directory and strings to replace.

        Args:
            directory (Path | str): The root directory to start the renaming process.
            old_str (str): The substring to be replaced in file names.
            new_str (str): The substring to replace with in file names.
        """
        if directory is None:
            directory = Path(input("Enter the directory path: "))
        
        if not isinstance(directory, Path):
            directory = Path(directory)
        if not directory.is_dir():
            raise ValueError("The provided path is not a valid directory!")
        
        self.directory = directory
        self.old_str = old_str
        self.new_str = new_str
        
        self.renamed_files = []
    
    def rename_files(self) -> None:
        """
        Renames files by replacing occurrences of old_str with new_str in their names
        within the specified directory and its subdirectories.
        """
        for file_path in (pbar:=tqdm(self.directory.rglob(f'*{self.old_str}*'), desc="Renaming files")):
            if not file_path.is_file():
                continue
            new_file_name = file_path.name.replace(self.old_str, self.new_str)
            new_file_path = file_path.with_name(new_file_name)
            
            self.renamed_files.append((file_path, new_file_path))
            pbar.set_postfix({"Renaming": f"{file_path.name} -> {new_file_name}"})
            
            file_path.rename(new_file_path)
        
        pbar.close()
        
        print("Renaming completed. Summary of changes:")
        for old_path, new_path in self.renamed_files:
            print(f"{old_path} -> {new_path}")
            
    def undo_rename(self) -> None:
        """
        Undoes the renaming by swapping new_str back to old_str in the renamed files.
        """
        for old_path, new_path in self.renamed_files:
            new_path.rename(old_path)
        print("Undo completed. Files have been restored to their original names.")
        
        self.renamed_files.clear()