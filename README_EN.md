# photo_organizer
[中文](/README.md) 

## Project Introduction
**Photo Organizer** is a Python-based photo organization tool primarily used for organizing JPG / RAW files captured by cameras (currently supports **SONY** by default).  
This tool fits into a photographer's culling workflow: first separate JPGs and RAWs, then cull within the JPGs, and finally clean up the unselected RAW files.  

The program automatically determines the current state based on the file structure:
* **Unclassified State**:
  * The root directory contains both JPG and RAW files.
  * The program automatically organizes them into `jpg` and `raw` folders.
  ```text
  Photos/
  ├─ DSC0001.JPG
  ├─ DSC0001.ARW
  ├─ DSC0002.JPG
  └─ DSC0002.ARW
  ```

* **Classified State**:
  * The root directory already contains `jpg` and `raw` folders.
  ```text
  Photos/
  ├─ jpg/
  │   ├─ DSC0001.JPG
  │   └─ DSC0002.JPG
  └─ raw/
      ├─ DSC0001.ARW
      └─ DSC0002.ARW
  ```
  * The program compares filenames between the two and moves **files that exist in RAW but not in JPG** to the `del` folder.
  ```text
  Photos/
  ├─ jpg/
  │   └─ DSC0001.JPG
  ├─ raw/
  │   └─ DSC0001.ARW
  └─ del/
      └─ DSC0002.ARW
  ```
> **Note**  
> This tool does not actually delete any files; it only moves them to the appropriate folders.

## Usage
### Requirements
* Python 3.10 or above
* Standard library only (no additional dependencies required)

### How to Run
#### 1. Drag and Drop (Recommended)
Drag the target photo folder directly onto the script file.

#### 2. Command Line
```bash
python phphoto_organizer.py [path_to_folder]
# If run without a file path, it enters interactive mode, prompting for manual path input.
```

### Advanced Configuration
#### 1. dry_run Mode
In dry_run mode, the program only outputs the planned move operations without actually moving files, to prevent loss from misoperation.  
dry_run mode is enabled by default. It is recommended to first review the output when using it for the first time, and then disable it after confirmation.  

#### 2. Configuration File config.py
`config.py` is the program's main configuration file, storing the dry_run mode setting, language mode, camera type, file extensions, and folder names.  
In most cases, users do not need to modify the main script. Modifying `config.py` allows for permanent adjustment of the program's behavior.  

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `DRY_RUN` | Whether to enable dry_run mode | `True` (Recommended to change to `False` when in use) |
| `LANGUAGE_MODE` | Language mode: BOTH / CN / EN (Bilingual / Chinese / English) | `BOTH` |
| `CFG_CAMERA` | Camera type | `SONY` |
| `CFG_EXTS` | File extensions for each camera. Extensible. To support other brands (Canon, Nikon, etc.), simply add the corresponding configuration. | N/A |
| `DIR_NAME_JPG` | JPG folder name. | `jpg` |
| `DIR_NAME_RAW` | RAW folder name. | `raw` |
| `DIR_NAME_DEL` | Folder name for filtered RAW files. | `del` |

> **Note**  
> After modifying `config.py`, the new default values will be used for each program run.  
> Users can also override some configurations via CLI parameters for flexible control of a single run's behavior.

#### 3. Command Line Parameters
Command-line parameters allow for targeted configuration of each run.

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `path` | Target folder path. If not provided, enters interactive mode; if input is `config`, modifies the configuration file. | None |
| `--dryrun` | When this flag is added, dry_run mode is enabled; if not added, the configuration file setting is used. | None |
| `--camera` | Camera type. | `SONY` |
| `--lang` | Language mode: BOTH / CN / EN (Bilingual / Chinese / English). | `BOTH` |

**Usage Examples**
```bash
# Run with default configuration
python phphoto_organizer.py [path_to_folder]

# Open config.py for editing
python phphoto_organizer.py config

# Run in dry_run mode
python phphoto_organizer.py [path_to_folder] --dryrun

# Specify camera type and language
python phphoto_organizer.py [path_to_folder] --camera CANON --lang EN
python phphoto_organizer.py [path_to_folder] --camera=CANON --lang=EN
```

> **Note**  
> The configuration file `config.py` is for long-term default settings; CLI parameters are suitable for temporary adjustments.  
> CLI parameters have higher priority than config.py, are only effective for the current run, and do not modify the configuration file.  
> The `config` subcommand directly opens the configuration file, and the main program then exits without performing any classification operations.  
