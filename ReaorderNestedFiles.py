import os, shutil, logging
logging.basicConfig(level=logging.DEBUG)

###########################################################################
## Commission: reorder all files in nested folders to a top level directory
## preserving the original name plus origianl folder name as prefix.
##
##
## Python 3.6 on Windows.
## Autor: Martin Eías Iglesias - 2020
###########################################################################

os.system('cls' if os.name == 'nt' else 'clear')
inital_warning = input("\nThese program will reorder and move all files in these folder and nested sub-folders to a new ordered-folder with a posfix name added.\nDo you want to continue?\nHit 'Enter key' to continue or type 'N' to cancel:\n" ) or True

cwd_name = os.path.basename(os.getcwd())
posfix_folder = "_ordenados"
new_dest_folder = f"{os.path.dirname(__file__)}\\{cwd_name}{posfix_folder}"


def get_items_list(base_path):
    # Find files into folders and subfolders.
    items_in_folders = []
    # Message from user when he reject the initial prompt.
    if inital_warning is not True:
        logging.info("\n"*2+" You choose cancel.\nThat program will be stopped and nothing will happen with your files.\nbye!\n\n")
        exit()

    # Say to the user where is the root folder.
    logging.info('\n'+f"Start working from {cwd_name}")
    def recursive_scan_folders(base_path):
        # Recursive start to find files.
        with os.scandir(base_path) as folder:
            if folder is not None:
                for content in folder:
                    currentpath = os.path.dirname(content)
                    if content.is_file() and content.name != os.path.basename(__file__):
                        dirname = os.path.dirname(content).rsplit("\\")[-1]
                        items_in_folders.append(f'{dirname}_{content.name}')
                        new_file_name = f'{dirname}_{content.name}'
                        # Create a folder where to files will be copy in order.
                        os.makedirs(new_dest_folder, exist_ok=True)
                        if posfix_folder not in str(dirname):
                            shutil.copy(f"{currentpath}\\{content.name}", f"{os.path.abspath(new_dest_folder)}\\{new_file_name}") # Move files from this folder to top root folder.
                    elif content.is_dir():
                        logging.info("\t"f'{content.name} It is a folder and not will be reordered.')
                        yield from recursive_scan_folders(content.path)
            else:
                logging.info('Sorry! \n No files or foldes in this path')

    for i in recursive_scan_folders(base_path):
        next(recursive_scan_folders(i.path))

    return items_in_folders

if __name__ == '__main__':
    logging.info('\n'+f"Files ordered are: {get_items_list(os.getcwd())}"+"\n"+f"on the new folder named: {new_dest_folder}")