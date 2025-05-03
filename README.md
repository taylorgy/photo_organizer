# photo_organizer_sony
> Python 3.10.6

This project is a Python-based photo organizer designed for SONY Cameras.It allows users to drag and drop a folder containing photo and raw files, and the program will classify the files into different folders accordingly. After filtering the photos, the program will also remove the corresponding raws.  
Supported cameras: SONY.

## Workflow
1. Read all files in a folder, which are `.jpg` photos and `.arw` raws (for SONY cameras), with same names mixed together.
2. Classify the photos into corresponding \[jpg\] or \[raw\] folders according to the extensions.
3. After filtering the photos in the \[jpg\] folder, traverse both folders and move unselected raws into the \[delete\] folder.
4. After organizing all the photos, the folder will be popped up.

## Usage
1. **Drag and Drop**: You can drag a folder containing your files onto the `photo_orginazer_sony.py` file to start.
2. **Follow the Instructions**: Simply follow the instructions and select the options to finish the organization process.
