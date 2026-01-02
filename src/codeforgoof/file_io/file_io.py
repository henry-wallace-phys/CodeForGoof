from pathlib import Path
from tqdm import tqdm
from typing import Optional

def iteratively_replace_file_name(directory: Path | str, old_str: str=" ", new_str: str="_") -> None:
    """
    Iteratively replaces occurrences of old_str with new_str in file names
    within the specified directory and its subdirectories.

    Args:
        directory (Path): The root directory to start the renaming process.
        old_str (str): The substring to be replaced in file names.
        new_str (str): The substring to replace with in file names.
    """
    if not isinstance(directory, Path):
        directory = Path(directory)
    if not directory.is_dir():
        raise ValueError("The provided path is not a valid directory!")
    
    renamed_files = []
    
    for file_path in (pbar:=tqdm(directory.rglob(f'*{old_str}*'), desc="Renaming files")):
        if not file_path.is_file():
            continue
        new_file_name = file_path.name.replace(old_str, new_str)
        new_file_path = file_path.with_name(new_file_name)
        
        renamed_files.append((file_path, new_file_path))
        pbar.set_postfix({"Renaming": f"{file_path.name} -> {new_file_name}"})
        
        file_path.rename(new_file_path)
        
    pbar.close()
    
    print("Renaming completed. Summary of changes:")
    for old_path, new_path in renamed_files:
        print(f"{old_path} -> {new_path}")


def interactive_rename(old_str: str=" ", new_str: str="_") -> None:
    '''
    Interactively prompts the user for a directory path and renames files
    by replacing occurrences of old_str with new_str in their names.
    Args:
        old_str (str): The substring to be replaced in file names.
        new_str (str): The substring to replace with in file names.
    '''
    path = Path(input("Enter the directory path: "))
    if not path.is_dir():
        print("The provided path is not a valid directory!")
        return
    
    iteratively_replace_file_name(path, old_str, new_str)
    
def rename_stuff(directory: Optional[Path | str]=None, old_str: str=" ", new_str: str="_") -> None:
    '''
    Renames files by replacing occurrences of old_str with new_str in their names.
    If no directory is provided, it prompts the user for a directory path.
    '''
    if directory is None:
        interactive_rename(old_str, new_str)
    else:
        iteratively_replace_file_name(directory, old_str, new_str)