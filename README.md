# adif-to-kml

A simple Python application to convert radio amateur ADIF data into KML for mapping and visualization. This tool features an easy-to-use graphical interface built with Tkinter.

## Features

- **ADIF to KML Conversion**: Easily transform your Amateur Data Interchange Format (ADIF) logs into Keyhole Markup Language (KML) files for use in mapping applications like Google Earth.
- **User-Friendly GUI**: Built with Tkinter, making it accessible for users of all experience levels.
- **Cross-platform**: Works on Windows, macOS, and Linux (requires Python). For Windows, there is an executable (.exe) file.

## Requirements

- Python 3.7 or later
- Tkinter (usually included with Python)

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/paddiedi/adif-to-kml.git
   cd adif-to-kml
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the GUI to select your ADIF file and choose a location for the generated KML file.

## Building a Standalone Windows Executable (.exe)

To create a standalone executable for Windows, you can use [PyInstaller](https://pyinstaller.org/):

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
   - `--onefile`: Package everything into a single .exe.
   - `--windowed`: Prevents a console window from appearing (ideal for GUI apps).

3. The generated executable will be found in the `dist/` directory.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Thx OH5RW for the inspiration.
- Built using Python and Tkinter.

---

**Cheers**
