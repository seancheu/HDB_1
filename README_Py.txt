-- For Python --
Contains an .exe file for HDB Flat Recommender App. Double clicking on the .exe will run the Python script in a packaged virtual environment with relevant libraries/packages.
This .exe was built with PyInstaller

**HDB_Final.py is the source code

-- HDB_Final.spec file tells PyInstaller how to process your script. It encodes the script names and most of the options you give to the pyinstaller command. The spec file is actually executable Python code. PyInstaller builds the app by executing the contents of the spec file. --

-- How to run HDB_Final.exe --
Double clicking the exe will open up a UI that allows users to select the .csv file to read data.
**ALL Prices 1990-2021 mar.csv**

After .csv has been opened, the next UI will allow users to select their Preferred Towns, Flat Types and enter their Budget ($).
The Recommendation window below will show the closest match to their criteria.

Versions:
Python 3.9.7
PyInstaller 
PySimpleGUI 4.60.4
Pandas 1.5.3
Numpy 1.24.2

Exclusions:
pyinstaller HDB_Final.py --upx-dir "C:\Users\Test account\Desktop\for_test1\upx-4.0.2-win64"--best --noconfirm --windowed --onefile --clean --exclude-module pyinstaller --exclude-module pip --splash "C:\Users\Test account\Desktop\DSC\M7\The Raizers\Reference Files\not_hdb.PNG" --hidden-import=pyi_splash

What is PyInstaller?
PyInstaller lets you freeze your python application into a stand-alone executable. This installer supports Linux, macOS, Windows, and more; and is also compatible with 3rd-party Python modules, such as PySide6.

https://doc.qt.io/qtforpython/deployment-pyinstaller.html#:~:text=PyInstaller%20lets%20you%20freeze%20your,Python%20modules%2C%20such%20as%20PySide6.

https://pyinstaller.org/en/stable/