# TODO:
#    [/] set up .ignore file
#    [ ] allow to unlink files/folders
#    [ ] conflict management
#    [ ] pass arguments
#        [/] -d / --delete  |  delete the symlink, then move the file/folder back
#        [/] -h / --help    |  print help info
#        [ ] -ei / --edit-ignore  |  edit ignore file
#        [ ]    / null      |  refresh the dotfile folder
#    [ ] docmentation
#    [ ] print help txt from file
#    [ ] name prgm (dottle, dotty/dottie, dottsy/dottsie)
#    [ ] add folder support for .dotty-ignore
#    [ ] user error handling
from pathlib import Path
import os
import argparse
import shutil

# source path (where the files will be)
source_root = Path.home() / ".dotfiles-test"

# enable argument parser (without abbreviations)
parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False)

# create optional arguments 
parser.add_argument("--delete", "-d", action="store_true")
parser.add_argument("--delete-full", "-df", action="store_true")
parser.add_argument("--edit-ignore", "-ei", action="store_true")
parser.add_argument("--help", "-h", action="store_true")

# create positional arguments
parser.add_argument("file", nargs="?", default=None)


args = parser.parse_args() # parse arguments


def normal_flag():

    # ignore file (inside source path)
    ignore_file = source_root / ".dotty-ignore"
    
    # convert lines in ignore file into a set
    ignored = set(
        line.strip()
        for line in ignore_file.read_text().splitlines()
        if line.strip() and line[0] != "#" 
    )
    
    # target path (where the file will be gotten from)
    target_root = Path.home()
    
    # recursively searches for each file in the source directory
    for path in source_root.rglob("*"):
    
        if not path.is_file(): # checks if it is a file (no folders)
            continue
    
        # the path of the file without $HOME
        relative = path.relative_to(source_root)
    
        # query ignored files file, stop if true
        if str(relative) in ignored:
            continue
    
        # the path of the file to symlink
        target = target_root / relative
    
        # makes the directory path for the file
        target.parent.mkdir(parents=True, exist_ok=True)
    
        # deletes the target file if it exists or is a symlink
        if target.exists() or target.is_symlink():
            target.unlink()
    
        # path of the target without specifying $HOME
        rel_target = os.path.relpath(path, start=target.parent)
    
        # symlink the target using the relative string
        target.symlink_to(rel_target)


    print("default mode enabled")


# print the help message
def help_flag():
    help_text = (
        "Commands available:\n\n"
        "--help        -h   print this text\n"
        "--delete      -d   copy file/folder back to origanal path and remove symlink\n"
        "--edit-ignore -ei  edit .dotty-ignore")
    print(help_text)

# this function does three things:
# 1. delete the symlink.
# 2. copy the file from .dotfiles to where the symlink was.
# 3. perform an unholy amount of checks to ensure 1 and 2 succeed.
#    checks include:
#    - if the path is absolute (or begins with ~)
#    - if the file exists in .dotfiles
#    - if the target file is actually a symlink
#    - if the target file is symlinked to the source file
def delete_flag():

    # the file given by the user (the one in .dotfiles)
    source = args.file
    source_path = Path(source)

    # source root dir
    source_root = Path.home() / ".dotfiles-test"

    # check if the path is absolute (should be relative)
    if source.startswith("~") or source_path.is_absolute(): 
        return

    
    source_file = Path(source_root / source_path)
    source_file = source_file.resolve() # normalizes path

    # check that it exists in the .dotfile dir
    if not source_file.exists():

        # [ ] add folder support

        # this is the var that is outside .dotfiles
        # this calculates that (by removing the instance of the 
        # .dotfile folder)
        target_path = source_file.parts
        target_path = [part for part in target_path
                            if part != ".dotfiles-test"]
        target_path = Path(*target_path)

        # check if it is actually a symlink
        if target_path.is_symlink():
            print("and it is a symlink")

            # check if the symlink actully points to the file we are deleting
            if target_path.resolve() == source_file.resolve():
                print("and it is symlinked to the right file")

                # delete the symlink (target)
                target_path.unlink(missing_ok=True)
                
                # copy the source file back to the target path
                shutil.copy2(source_file, target_path)

    else:
        print("the file is NOT in", source_root)


# check for arg after --delete flag
if args.delete and args.file is None:
    parser.error("the file argument is required when --delete is used")

# cheeck for --delete flag
if args.delete:
    delete_flag()

elif args.help: # check for help flag
    help_flag()
else: # when no args are supplied (default behavior)
    normal_flag()

















