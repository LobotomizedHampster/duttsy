from pathlib import Path
import os
import argparse
import shutil
import sys

def main():
    def all_code():
        # source path (where the files will be)
        dotfile_folder = ".dotfiles"
        source_root = Path.home() / dotfile_folder
        
        # target path (where the file will be gotten from)
        target_root = Path.home()
    
        # folder for overwritten files
        overwritten_path = source_root / ".overwritten"

        # ignore file (inside source path)
        ignore_file = source_root / ".duttsy-ignore"
        
        
        # enable argument parser (without abbreviations)
        parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
        
        # create optional arguments 
        parser.add_argument("--delete", "-d", action="store_true")
        parser.add_argument("--help", "-h", action="store_true")
        parser.add_argument("--create-config", "-cc", action="store_true")
        
        # create positional arguments
        parser.add_argument("file", nargs="?", default=None)
        
        args = parser.parse_args() # parse arguments
    
    
        def normal_flag():
        
            print("normal flag selected")
        
            # ignore file (inside source path)
            ignore_file = source_root / ".dotty-ignore"
        
            # convert lines in ignore file into a set
            ignored = set(line.strip()
                for line in ignore_file.read_text().splitlines()
                if line.strip() and not line.strip().startswith("#") # ignore comments
                )
        
        
            for line in ignored.copy():
        
                real_line = line
                line = source_root / Path(line) # get fill path
        
                if line.is_dir(): # determine if directory
                    
                    for path in line.rglob("*"): # expand directories
                        if not Path(path).is_dir(): # omit subdirectories
                            
                            path = path.relative_to(source_root) 
                            # have to add to subfiles when in a loop due to iterable
                            # being a set and thus having no order
                            ignored.add(str(path))
        
                    ignored.remove(str(real_line)) # remove the folder line
        
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
                    if not target.read_bytes() == path.read_bytes():
                        print(f"WARNING:\n"
                              f"  {target}\n"
                              f"  is different than {path}\n" 
                              f"  moving to {overwritten_path}")
    
    
                        overwritten_target = overwritten_path / target.name
                        overwritten_path.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(target, overwritten_target)
    
                        #continue
                    target.unlink()
            
                # path of the target without specifying $HOME
                rel_target = os.path.relpath(path, start=target.parent)
            
                # symlink the target using the relative string
                target.symlink_to(rel_target)
        
        
        
        
        # print the help message
        def help_flag():
            help_text = (
                "Commands available:\n\n"
                "--help        -h   print this text\n"
                "--delete      -d   copy file/folder "
                "back to origanal path and remove symlink\n"
                "--edit-ignore -ei  edit .dotty-ignore")
            print(help_text)
        
        
        
        
        # this function does a couple things:
        # 1. delete the symlink.
        # 2. copy the file from .dotfiles to where the symlink was.
        # 3. determine if the argument is a file or folder
        #    - if its a folder, recursively loop through each file 
        #    - if its not, only apply the process to the one file
        # 4. perform an unholy amount of checks to ensure 1, 2, and 3 succeed.
        #    checks include:
        #    - if the path is absolute (or begins with ~)
        #    - if the file exists in .dotfiles
        #    - if the target file is actually a symlink
        #    - if the target file is symlinked to the source file
        def delete_flag():
        
            # the source file given by the user (the one in .dotfiles)
            source = args.file
            source_path = Path(source)
        
            # check if the path is absolute (should be relative)
            if source.startswith("~") or source_path.is_absolute(): 
                raise ValueError("provide a path that is relative to the dotfiles"
                                 " folder. see docs for more info")
        
            source_path = Path(source_root / source_path)
            source_path = source_path.resolve() # normalizes path
        
            # check that it exists in the .dotfile dir
            if not source_path.exists():
                raise FileNotFoundError("file was not found in dotfile directory")
        
        
            def unlink_and_copy(path):
                # this is the var that is outside .dotfiles
                # this calculates that (by removing the instance of the 
                # .dotfile folder)
                target_path = path.parts
                target_path = [part for part in target_path
                                    if part != dotfile_folder]
                target_path = Path(*target_path)
            
                # check if it is actually a symlink
                if not target_path.is_symlink():
                    print(f"WARNING: the file {target_path}"
                          "is not a symlink. skipping...")
                    return
    
                # check if the symlink actully points to the file we are deleting
                if not target_path.resolve() == path.resolve():
                    print(f"WARNING: the file {target_path} is "
                          "symlinked to a different file. skipping...")
                    return
            
                # delete the symlink (target)
                target_path.unlink(missing_ok=True)
                # copy the source file back to the target path
                shutil.copy2(path, target_path)
        
            # check if a dir
            if source_path.is_dir():
                print("is a dir")
        
                # recuseively loop through each file/subdirectory in a directory
                for path in source_path.rglob("*"):
        
                    # check for and omit directories
                    if not path.is_file():
                        continue
        
                    unlink_and_copy(path)
            else:
                unlink_and_copy(source_path)
        
        
        
        
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
    
    
    try:
        all_code()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
