from codeforgoof.file_io import rename_stuff

import argparse

def main():
    parser = argparse.ArgumentParser(description="Rename files by replacing substrings in their names.")
    parser.add_argument("directory", "-d", default=None, type=str, help="The root directory to start the renaming process.")
    parser.add_argument("old_str", "-o", default=" ", type=str, help="The substring to be replaced in file names.")
    parser.add_argument("new_str", "-n", default="_", type=str, help="The substring to replace with in file names.")
    args = parser.parse_args()

    rename_stuff(args.directory, args.old_str, args.new_str)

if __name__ == "__main__":
    main()
