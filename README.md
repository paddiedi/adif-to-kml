# adif-to-kml

A simple Python application to convert radio amateur ADIF data into KML for mapping and visualization. This tool features an easy-to-use graphical interface built with Tkinter.

## Features

- **ADIF to KML Conversion**: Easily transform your Amateur Data Interchange Format (ADIF) logs into Keyhole Markup Language (KML) files for use in mapping applications like Google Earth.
- **User-Friendly GUI**: Built with Tkinter, making it accessible for users of all experience levels.
- **Cross-platform**: Works on Windows, macOS, and Linux (requires Python).

## Requirements

- Python 3.7 or later
- Tkinter (usually included with Python)
- Standard Python libraries (no extra dependencies)

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/paddiedi/adif-to-kml.git
   cd adif-to-kml
   ```

2. Run the application:
   ```bash
   python adif_to_kml.py
   ```
   *Replace `adif_to_kml.py` with the actual main script name if different.*

3. Use the GUI to select your ADIF file and choose a location for the generated KML file.

## Building a Standalone Windows Executable (.exe)

To create a standalone executable for Windows, you can use [PyInstaller](https://pyinstaller.org/):

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller --onefile --windowed adif_to_kml.py
   ```
   - `--onefile`: Package everything into a single .exe.
   - `--windowed`: Prevents a console window from appearing (ideal for GUI apps).

3. The generated executable will be found in the `dist/` directory.

## Example

- **Input**: `logbook.adi` (ADIF file)
- **Output**: `logbook.kml` (KML file for mapping)

## Contributing

Pull requests, bug reports, and feature suggestions are welcome! Please open an issue or PR if you have ideas to improve this project.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by the needs of amateur radio operators who want to visualize their QSOs on maps.
- Built using Python and Tkinter.

---

**Happy Mapping!**
