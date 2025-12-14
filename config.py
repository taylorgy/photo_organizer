"""
用户配置文件
大多数用户无需修改主脚本
在此修改可以调整程序行为

User configuration file
Most users do NOT need to modify the main script
Change configs here to adjust behavior
"""
# 安全模式 / Dry-run mode
# True 表示仅模拟移动文件 / True = only simulate file move
DRY_RUN = True


# 语言模式 / Language mode
LANGUAGE_MODE = "BOTH" # BOTH / CN / EN


# -------- 相机配置 / Camera configuration --------
CFG_CAMERA = "SONY" # 当前相机 / Current camera


# 相机扩展名映射 / Camera extension mapping
CFG_EXTS = {
    "SONY": {
        "jpg": {".jpg"}, # 照片扩展名 / Photo file extensions
        "raw": {".arw"}, # RAW 文件扩展名 / RAW file extensions
    },
  # 未来扩展示例 / Example for future extension
    # "CANON": {
    #     "jpg": {".jpg", ".jpeg"},
    #     "raw": {".cr2", ".cr3"},
    # },
}


# 文件夹名称 / Folder names
DIR_NAME_JPG = "jpg" # JPG 文件夹 / JPG folder
DIR_NAME_RAW = "raw" # RAW 文件夹 / RAW folder
DIR_NAME_DEL = "del" # 过滤的 RAW 文件夹 / Folder for filtered RAW files