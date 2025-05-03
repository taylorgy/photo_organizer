# python=3.10.6
# coding=utf-8

'''
@File   phphoto_organizer.py
@Time   2025/04
@Author TaylorGy 
@Site   https://github.com/taylorgy
@Desc   This project is a Python-based photo organizer designed for SONY Cameras. It allows users to drag and drop a folder containing photo and raw files, and the program will classify the files into different folders accordingly. After filtering the photos, the program will also remove the corresponding raws.
Supported cameras: SONY.
'''

# import os
import sys
import subprocess
from pathlib import Path

def get_folder_path() -> str:
    '''
    Prompt user to input a valid folder path.
    Continues to ask until a valid path is provided or 'N' is entered to exit.
    '''
    while True:
        print("请输入 N 退出程序，将目标文件夹拖动到此脚本。")
        print("Please enter N to exit, then drag the folder onto this script.")
        dir_root = input("或输入文件夹路径：\nOr enter the folder path: ").strip()
        print()
        if not dir_root:
            continue  # Skip empty input
        if dir_root.lower() == 'n' or Path(dir_root).is_dir():
            return dir_root
        else:
            print("错误: 提供的路径不是有效的文件夹。")
            print("Error: The provided path is not a valid folder.")
            print()

def photo_classifier(dir_root: Path, camera: str) -> None:
    '''
    Classify photos and raws into separate folders based on the camera type.
    Supported cameras: SONY.    
    '''
    files = [f for f in dir_root.iterdir() if f.is_file()]  # Get all files in the directory
    count_files = len(files)  # Count the number of files
    print(f"根目录文件数量：{count_files}。")
    print(f"Number of files in the root directory: {count_files}.")
    print()

    if count_files == 0:
        print("无需进行分类。")
        print("Classification not needed.")
        print()
        return None
    else:
        print("正在进行分类...")
        print("Classification in progress...")
        print()
        # Define the file extensions for photos and raws
        if camera == 'SONY':
            # ext_photo = ['.jpg', '.jpeg', '.png']
            # ext_raw = ['.arw', '.srf', '.sr2']
            ext_jpg = ['.jpg']
            ext_raw = ['.arw']

        # Create folders for photos and raws
        dir_jpg = dir_root / 'jpg'
        dir_raw = dir_root / 'raw'
        dir_jpg.mkdir(exist_ok=True)
        dir_raw.mkdir(exist_ok=True)

        # print(len(files))
        # Walk through the directory and organize all files
        for file in files:
            # Filter out the photo and raw files
            if file.suffix.lower() in ext_jpg:
                file.rename(dir_jpg / file.name)  # Move the photo file to the jpg folder
            elif file.suffix.lower() in ext_raw:
                file.rename(dir_raw / file.name)  # Move the raw file to the raw folder

    print("分类完成！")
    print("Classification completed.")
    print()
    return None

def raw_filter(dir_root: Path) -> None:
    '''
    Filter raws that do not have corresponding photos.
    The photos and raws use the same name but different extensions.
    '''

    # Create folders for photos and raws
    dir_jpg = dir_root / 'jpg'
    dir_raw = dir_root / 'raw'
    dir_del = dir_root / 'del'
    dir_del.mkdir(exist_ok=True)
    
    stems_jpg = {f.stem for f in dir_jpg.iterdir() if f.is_file()}  # Get the stems of photos
    stems_raw = {f.stem for f in dir_raw.iterdir() if f.is_file()}  # Get the stems of raws
    stems_del = stems_raw - stems_jpg  # Get the stems of raws to be filtered

    if not stems_del:
        print("请先筛选 jpg 文件夹中的照片，然后再次运行程序。")
        print("Please run the program again after filtering the jpg folder.")
        print()
    else:
        # Walk through the directory and filter raw files without corresponding photos
        for file in dir_raw.iterdir():
            if file.stem in stems_del:
                file.rename(dir_del / file.name)  # Move the raw file to the del folder

    print(f"已过滤 raw 文件数量： {len(stems_del)}。")
    print(f"Filtered raw files count: {len(stems_del)}.")
    print()
    return None

def main():
    # Check arguments and get the folder path
    camera = 'sony'
    dir_root = 'n'

    if len(sys.argv) == 1:
        # If script is executed directly
        dir_root = get_folder_path()

    elif len(sys.argv) == 2:
        # If folder is dragged onto the script
        dir_root = sys.argv[1]
        if not Path(dir_root).is_dir:
            dir_root = get_folder_path()
    else: 
        # In case of other usage
        dir_root = 'n'
    
    # Main processing
    if dir_root.lower() == 'n':
        # If N is entered, exit the program
        print("退出程序。")
        print("Exit the program.")
        print()
        # sys.exit(0)
        return None
    else:
        camera = camera.upper()
        print(f"欢迎使用照片整理工具。相机类型：{camera}")
        print(f"Welcome to the photo organizer. Camera type: {camera}")
        print()
        # If a valid folder path is provided, process the folder
        dir_root = Path(dir_root)
        # dir_root = Path(dir_root).resolve() # get the absolute path
        print(f"正在处理文件夹: {dir_root}")
        print(f"Processing folder: {dir_root}")
        print()

        photo_classifier(dir_root, camera)

        raw_filter(dir_root)

        input("按回车键退出。\nPress Enter to exit.")

if __name__ == "__main__":
    main()
