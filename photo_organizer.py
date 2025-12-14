# python=3.10+
# coding=utf-8

"""
@File   photo_organizer.py
@Time   2025/12
@Author TaylorGy
@Site   https://github.com/taylorgy
@Desc
    照片自动分类整理工具，支持多种相机 RAW 格式（默认：SONY）。
    Photo automatic classification and organization tool supporting various camera RAW formats.
"""

import sys
import shutil
from pathlib import Path
import argparse
import os
from subprocess import Popen

# =========================
# Configurations
# =========================

from config import (
    CFG_CAMERA,
    CFG_EXTS,
    DIR_NAME_JPG,
    DIR_NAME_RAW,
    DIR_NAME_DEL,
    LANGUAGE_MODE,
    DRY_RUN
)


# =========================
# Helpers
# =========================

def print_cn_en(extra_blank_lines: int, cn: str, en: str) -> None:
    """
    根据 LANGUAGE_MODE 输出中英提示。
    Print Chinese and English prompts based on LANGUAGE_MODE.
    """
    if LANGUAGE_MODE in ("BOTH", "CN"):
        print(cn)
    if LANGUAGE_MODE in ("BOTH", "EN"):
        print(en)
    for _ in range(extra_blank_lines):
        print()


def get_folder_path() -> str:
    """
    CLI 提示用户输入文件夹路径，支持拖拽文件夹到脚本。
    Prompt user to input folder path via CLI, supports drag-and-drop.
    """
    while True:
        print_cn_en(0, 
            "1. 输入 N 退出程序，再将目标文件夹拖动到此脚本。",
            "1. Enter N to exit, and drag the target folder onto this script."
        )
        print_cn_en(0, 
            "2. 请输入文件夹路径：", 
            "2. Please enter the folder path:"
        )
        dir_root = input().strip()
        print()

        if not dir_root:
            continue
        if dir_root.lower() == "n" or Path(dir_root).is_dir():
            return dir_root

        print_cn_en(1, 
            "错误：提供的路径不是有效的文件夹。",
            "Error: The provided path is not a valid folder."
        )


def suffix_lower(p: Path) -> str:
    """
    获取文件扩展名的小写形式
    Return lowercase file suffix
    """
    return p.suffix.lower()


# =========================
# State Detection
# =========================

def is_unclassified(root: Path, exts_jpg: set, exts_raw: set) -> bool:
    """
    检测文件夹是否未分类。
    Check if folder is unclassified.
    """
    has_jpg = any(
        p.is_file() and suffix_lower(p) in exts_jpg
        for p in root.iterdir()
    )
    has_raw = any(
        p.is_file() and suffix_lower(p) in exts_raw
        for p in root.iterdir()
    )
    return has_jpg and has_raw


def is_classified(root: Path) -> bool:
    """
    检测文件夹是否已分类。
    Check if folder is classified.
    """
    return (root / DIR_NAME_JPG).is_dir() and (root / DIR_NAME_RAW).is_dir()


# =========================
# Core Logic
# =========================

def classify_files(root: Path, exts_jpg: set, exts_raw: set) -> {int, int}:
    """
    分类文件到 JPG 和 RAW 文件夹，并返回各自数量。
    Classify files into JPG and RAW folders, returning their counts.
    """
    print_cn_en(0, 
        "正在进行分类...",
        "Classification in progress..."
    )
    dir_jpg = root / DIR_NAME_JPG
    dir_raw = root / DIR_NAME_RAW
    if DRY_RUN:
        print_cn_en(0, 
            f"[DRY RUN] 创建文件夹：{dir_jpg}, {dir_raw}",
            f"[DRY RUN] Create folders: {dir_jpg}, {dir_raw}"
        )
    else:
        dir_jpg.mkdir(exist_ok=True)
        dir_raw.mkdir(exist_ok=True)

    count_jpg = 0
    count_raw = 0

    for f in root.iterdir():
        if not f.is_file():
            continue

        ext = suffix_lower(f)
        if ext in exts_jpg:
            count_jpg += 1
            if DRY_RUN:
                print_cn_en(0, 
                    f"[DRY RUN] 移动文件：{f.name} -> {dir_jpg}",
                    f"[DRY RUN] Move file: {f.name} -> {dir_jpg}"
                )
            else:
                shutil.move(str(f), dir_jpg / f.name)
        elif ext in exts_raw:
            count_raw += 1
            if DRY_RUN:
                print_cn_en(0, 
                    f"[DRY RUN] 移动文件：{f.name} -> {dir_raw}",
                    f"[DRY RUN] Move file: {f.name} -> {dir_raw}"
                )
            else:
                shutil.move(str(f), dir_raw / f.name)

    print_cn_en(0, 
        "分类完成。",
        "Classification completed."
    )
    print_cn_en(0, 
        f"JPG 文件数量：{count_jpg}",
        f"JPG files: {count_jpg}"
    )
    print_cn_en(1,
        f"RAW 文件数量：{count_raw}",
        f"RAW files: {count_raw}"
    )
    return count_jpg, count_raw


def filter_raw_files(root: Path, exts_jpg: set, exts_raw: set) -> int:
    """
    过滤 RAW 文件：仅保留有对应 JPG 的 RAW，返回移动到 DEL 文件夹的数量。
    Filter RAW files: keep only RAWs with matching JPGs, and return count of moved RAW files.
    """
    dir_jpg = root / DIR_NAME_JPG
    dir_raw = root / DIR_NAME_RAW
    dir_del = root / DIR_NAME_DEL
    if DRY_RUN:
        print_cn_en(0, 
            f"[DRY RUN] 创建文件夹：{dir_del}",
            f"[DRY RUN] Create folder: {dir_del}"
        )
    else:
        dir_del.mkdir(exist_ok=True)

    stems_jpg = {
        f.stem for f in dir_jpg.iterdir()
        if f.is_file() and suffix_lower(f) in exts_jpg
    }
    stems_raw = {
        f.stem for f in dir_raw.iterdir()
        if f.is_file() and suffix_lower(f) in exts_raw
    }

    stems_del = stems_raw - stems_jpg

    if not stems_del:
        print_cn_en(1, 
            "未发现需要过滤的 RAW 文件。",
            "No RAW files to filter."
        )
        return 0
    
    print_cn_en(0, 
        "正在过滤 RAW 文件...",
        "Filtering RAW files..."
    )
    for f in dir_raw.iterdir():
        if f.is_file() and f.stem in stems_del:
            if DRY_RUN:
                print_cn_en(0, 
                    f"[DRY RUN] 移动文件：{f.name} -> {dir_del}",
                    f"[DRY RUN] Move file: {f.name} -> {dir_del}"
                )
            else:
                shutil.move(str(f), dir_del / f.name)
    print_cn_en(0, 
        "RAW 文件过滤完成。",
        "RAW file filtering completed."
    )
    print_cn_en(1, 
        f"已过滤 RAW 文件数量：{len(stems_del)}",
        f"Filtered RAW files count: {len(stems_del)}"
    )
    return len(stems_del)


# =========================
# Main Entry
# =========================

def main():
    """
    主程序入口。
    Main program entry.
    """
    global DRY_RUN, LANGUAGE_MODE
    # -------- command line arguments --------
    parser = argparse.ArgumentParser(description="照片整理工具 / Photo Organizer")
    parser.add_argument(
        "path", 
        nargs="?", 
        help="目标文件夹路径（输入'config'修改默认设置）/ Target folder path (type 'config' to change settings)"
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="启用安全模式，仅模拟文件移动 / Enable dry-run mode, only simulate file moves"
    )
    parser.add_argument(
        "--camera",
        type=str,
        default=CFG_CAMERA,
        help="相机类型（默认为 SONY） / Camera type (default: SONY)"
    )
    def _type_lang(x):
        if x.upper() not in ("BOTH", "CN", "EN"):
            raise argparse.ArgumentTypeError("语言选项为 BOTH | CN | EN / Language options are BOTH | CN | EN")
        return x.upper()
    parser.add_argument(
        "--lang",
        type=_type_lang,
        choices=["BOTH", "CN", "EN"],
        default=LANGUAGE_MODE,
        help="语言模式：[BOTH] | CN | EN / Language mode: [BOTH] | CN | EN"
    )
    args = parser.parse_args()

    # -------- path --------
    dir_root = ""
    if args.path:
        if args.path == "config":
            dir_root = Path(__file__).parent / "config.py"
            print_cn_en(1, 
                "正在打开配置文件：config.py，请修改后重新运行程序。",
                "Opening configuration file: config.py, please modify and rerun the program."
            )
            if sys.platform.startswith("win"):
                Popen(["notepad", str(dir_root)])
            elif sys.platform == "darwin":
                Popen(["open", "-t", str(dir_root)])
            else:
                Popen(["xdg-open", str(dir_root)])
            dir_root = "n"  # 退出程序 / exit program
        else:
            if Path(args.path).is_dir():
                dir_root = args.path

    if not dir_root:
        dir_root = get_folder_path()

    if dir_root.lower() == "n":
        print_cn_en(1, 
            "程序已退出。",
            "Program exited."
        )
        return

    root = Path(dir_root)

    # -------- DRY RUN --------
    DRY_RUN = bool(args.dryrun)

    # -------- LANGUAGE MODE --------    
    if args.lang:
        LANGUAGE_MODE = args.lang.upper()

    # -------- CAMERA  --------
    camera = args.camera.upper()
    if camera not in CFG_EXTS:
        print_cn_en(1, 
            f"不支持的相机类型：{camera}", 
            f"Unsupported camera type: {camera}")
        return

    exts_jpg = CFG_EXTS[camera]["jpg"]
    exts_raw = CFG_EXTS[camera]["raw"]

    print_cn_en(0, 
        "欢迎使用照片整理工具。",
        "Welcome to the photo organizer."
    )
    print_cn_en(0, 
        f"相机类型：{camera}", 
        f"Camera type: {camera}"
    )
    print_cn_en(1, 
        f"安全模式：{'开启' if DRY_RUN else '关闭'}",
        f"Dry-run mode: {'ON' if DRY_RUN else 'OFF'}"
    )

    print_cn_en(1, 
        f"正在处理文件夹：{root}",
        f"Processing folder: {root}"
    )

    if is_unclassified(root, exts_jpg, exts_raw):
        classify_files(root, exts_jpg, exts_raw)
    elif is_classified(root):
        filter_raw_files(root, exts_jpg, exts_raw)
    else:
        print_cn_en(1, 
            "无法识别当前文件夹状态。",
            "Unable to determine the folder state."
        )
        return

    print_cn_en(0, 
        "处理完成。按回车键退出。",
        "Process completed. Press Enter to exit."
    )
    input()


if __name__ == "__main__":
    main()
