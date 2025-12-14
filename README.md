# photo_organizer
[English](/README_EN.md) 

## 项目简介
**Photo Organizer** 是一个基于 Python 的照片整理工具，主要用来整理相机拍摄的 JPG / RAW，在 文件（当前默认支持 **SONY**）。  
该工具适合摄影师的筛片流程：先分离 JPG 与 RAW，在 JPG 中筛选后清理未被选中的 RAW。  

程序会根据文件结构自动判断当前状态：
* **未分类状态**：
  * 根目录中同时存在 JPG 与 RAW 文件
  * 程序会自动将它们分别整理到 `jpg` 与 `raw` 文件夹中
  ```text
  Photos/
  ├─ DSC0001.JPG
  ├─ DSC0001.ARW
  ├─ DSC0002.JPG
  └─ DSC0002.ARW
  ```

* **已分类状态**：
  * 根目录中已存在 `jpg` 与 `raw` 文件夹
  ```text
  Photos/
  ├─ jpg/
  │   ├─ DSC0001.JPG
  │   └─ DSC0002.JPG
  └─ raw/
      ├─ DSC0001.ARW
      └─ DSC0002.ARW
  ```
  * 程序会对比两者文件名，将 **RAW 中存在但 JPG 中不存在的文件** 移动到 `del` 文件夹中
  ```text
  Photos/
  ├─ jpg/
  │   └─ DSC0001.JPG
  ├─ raw/
  │   └─ DSC0001.ARW
  └─ del/
      └─ DSC0002.ARW
  ```
> **说明**  
> 本工具不会实际删除任何文件，只会移动到相应的文件夹。  

## 使用方法
### 环境要求
* Python 3.10 或以上
* 标准库即可（无需额外依赖）

### 运行方式
#### 1. 拖拽运行（推荐）
将目标照片文件夹直接拖拽到脚本文件上。

#### 2. 命令行运行
```bash
python phphoto_organizer.py [path_to_folder]
# 若不输入文件路径直接运行，则会进入交互模式，提示手动输入路径。
```

### 进阶配置
#### 1. dry_run 模式
dry_run 模式下，程序只会输出移动操作，而不会实际移动文件，以免误操作造成损失。  
dry_run 模式默认开启，建议第一次使用时先查看效果，确认无误后再关闭。  

#### 2. 配置文件 config.py
`config.py` 是程序的主要配置文件，保存了 dry_run 模式设置，语言模式、相机类型、文件扩展名以及文件夹命名。  
大部分情况下，用户无需修改主脚本，通过修改 `config.py` 可以永久调整程序行为。

| 参数 | 说明 | 默认值 |
|-----|-----|-----|
| `DRY_RUN` | 是否启用 dry_run 模式 | `True`（建议使用时改为 `False`） |
| `LANGUAGE_MODE` | 语言模式：BOTH / CN / EN（双语 / 中文 / 英文）| `BOTH` |
| `CFG_CAMERA` | 相机类型 | `SONY` |
| `CFG_EXTS` | 各相机文件扩展名，可拓展，如需支持其他品牌（Canon、Nikon 等），只需添加对应配置即可。 | 无 | 
| `DIR_NAME_JPG` | JPG 文件夹名。 | `jpg` |
| `DIR_NAME_RAW` | RAW 文件夹名。 | `raw` |
| `DIR_NAME_DEL` | 被过滤的 RAW 文件夹名。 | `del` |

> **说明**  
> 修改 `config.py` 后，每次运行程序都会使用新的默认值。  
> 用户也可以通过 CLI 参数覆盖部分配置，灵活控制单次运行行为。

#### 3. 命令行参数
通过命令行参数，可以针对性地配置每一次运行。  
| 参数 | 说明 | 默认值 |
|------------|------------------|----------------|
| `path` | 目标文件夹路径。如不输入则会进入交互模式；若输入为 `config` 则会修改配置文件。| 无 |
| `--dryrun` | 添加此参数时，会启用 dry_run 模式；若未添加则使用配置文件设定。 | 无 |
| `--camera` | 相机类型 | `SONY` |
| `--lang` | 语言模式：BOTH / CN / EN（双语 / 中文 / 英文）| `BOTH` |

**使用示例**
```bash
# 使用默认配置运行
python phphoto_organizer.py [path_to_folder]

# 打开 config.py 进行修改
python phphoto_organizer.py config

# 以 dry_run 模式运行
python phphoto_organizer.py [path_to_folder] --dryrun

# 指定相机类型和语言
python phphoto_organizer.py [path_to_folder] --camera CANON --lang EN
python phphoto_organizer.py [path_to_folder] --camera=CANON --lang=EN
```

> **说明**  
> 配置文件 `config.py` 用于长期设置默认值；CLI 参数适合临时调整。  
> CLI 参数优先级高于 config.py，仅对当前运行有效，不会修改配置文件。  
> config 子命令会直接打开配置文件，主程序随即退出，不会进行任何分类操作。  



