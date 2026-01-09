# adif-to-kml

A simple Python application to convert radio amateur ADIF data into KML.

## Requirements

- Python 3.7 or later
- Tkinter

For Windows there's a exe. Other people than Windows users, can just download the repo and run it with python.

## Building with pyinstaller

To create a standalone executable for Windows, you can use [PyInstaller](https://pyinstaller.org/):

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```
2. **Build the executable**:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
3. The generated executable will be found in the `dist/` directory.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Thx OH5RW for the inspiration.

---

**Cheers**
