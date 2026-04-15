# TODO:
#    [/] set up .ignore file
#    [ ] allow to unlink files/folders
#    [ ] conflict management
#    [ ] pass arguments
#        [ ] -d / --delete  |  delete the symlink, then move the file/folder back
#        [ ] -h / --help    |  print help info
#        [ ] -ei / --edit-ignore  |  edit ignore file
#        [ ]    / null      |  refresh the dotfile folder
#    [ ] docmentation
#    [ ] print help txt from file
#    [ ] name prgm (dottle, dotty/dottie, dottsy/dottsie)
#    [ ] add folder support for .dotty-ignore
from pathlib import Path
import os
import argparse

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
parser.add_argument("file")


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



def help_flag():
    help_text = (
        "Commands available:\n\n"
        "--help        -h   print this text\n"
        "--delete      -d   copy file/folder back to origanal path and remove symlink\n"
        "--edit-ignore -ei  edit .dotty-ignore")
    print(help_text)


def delete_flag():
    target = args.file
    target_path = Path(target)

    if target.startswith("~"): # expand "~" into "/home/user/"
        deleted_file = target_path.expanduser()

    elif not target_path.is_absolute(): # if the path is relative
        cwd = Path.cwd() # current directory
        deleted_file = str(cwd / target)

    else: # if the path is absolute
        deleted_file = target

    # source path (where the files will be)
    source_root = Path.home() / ".dotfiles-test"


    deleted_file = Path(deleted_file)
    deleted_file = deleted_file.resolve() # normalizes path

    # debug print
    print("delete mode enabled, deleting:", deleted_file)
    print("file type:", type(deleted_file))

    # check if file is in the dotfile dir (failsafe)
    if source_root in deleted_file.parents or deleted_file == target:
        print("the file IS in", source_root)
        # now i need to:
        # [ ] should check if file is symlink
        # [/] check if the file is symlinked to **the file we are unlinking**
        # [ ] delete the symlink
        # [ ] copy the file back to origanal place
        # [ ] get the orignal string
        deleted_path = list(deleted_file.parts)
        parts
        print("parts of the deleted file path:", list(deleted_file.parts))
        #print("the symlink is in:", symlink_path)

    else:
        print("the file is NOT in", source_root)




if args.delete: # check for delete flag
    delete_flag()

elif args.help: # check for help flag
    help_flag()
else: # when no args are supplied (default behavior)
    normal_flag()
