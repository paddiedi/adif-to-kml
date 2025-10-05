import tkinter as tk
from tkinter import filedialog, messagebox
import grid
import re
entry_dictionary_id = [
    "CALL",
    "QSO_DATE",
    "TIME_ON",
    "TIME_OFF",
    "ARRL_SECT",
    "BAND",
    "STATION_CALLSIGN",
    "FREQ",
    "CONTEST_ID",
    "FREQ_RX",
    "MODE",
    "RST_RCVD",
    "RST_SEND",
    "TX_PWR",
    "OPERATOR",
    "GRIDSQUARE",
    "CQZ",
]
earth_entries = []
def upload_file():
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        messagebox.showinfo("File Selected", f"You selected: {file_path}")
        return file_path
    return None

def extract_adif_kml(file_path):
  with open(file_path) as f:
    data = []
    for line in f:
        entry_dictionary = {key: "" for key in entry_dictionary_id}
        entries = line.split()
        for i in entries:
            for name in entry_dictionary_id:
                stripped = i.strip()
                if stripped.startswith(f"<{name}:"):
                    print(stripped)
                    # Look for where the > char is
                    start_index = stripped.index(">")
                    entry_dictionary[name] = stripped[(start_index + 1):]
                else:
                    pass
        data.append(entry_dictionary)
    return data
def convert_into_kml(entries, name, description):
    with open("output.kml", "w") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{name}</name>
    <description>{description}</description>

    <!-- Optional Style for CW QSOs -->
    <Style id="CWStyle">
      <IconStyle>
        <color>ff00ff00</color> <!-- Green -->
        <scale>1.2</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
        </Icon>
      </IconStyle>
    </Style>""")
        for entry in entries:
            coords = grid.calc_coords(entry["GRIDSQUARE"])
            kml_template = f"""
<Placemark>
  <name>{entry["CALL"]}</name>
  <description>
    <![CDATA[
    QSO Date: {entry["QSO_DATE"]}<br/>
    Time On: {entry["TIME_ON"]}<br/>
    Time Off: {entry["TIME_OFF"]}<br/>
    Band: {entry["BAND"]}<br/>
    Frequency:{entry["FREQ"]} MHz<br/>
    Mode: {entry["MODE"]}<br/>
    RST Received: {entry["RST_RCVD"]}<br/>
    Power: {entry["TX_PWR"]}<br/>
    Operator: {entry["OPERATOR"]}<br/>
    Contest: {entry["CONTEST_ID"]}<br/>
    CQ Zone: {entry["CQZ"]}
    ]]>
  </description>
  <Point>
    <coordinates>{coords[0]},{coords[1]},0</coordinates>
  </Point>
</Placemark>"""
            f.write(kml_template)
        f.write("\n</Document>\n</kml>")
def render_window():
    # Create the main window
    root = tk.Tk()
    root.title("ADIF-KML CONVERTER")
    root.geometry("400x300")

    # Add a label
    label = tk.Label(root, text="ADIF-KML CONVERTER", font=("Arial", 14))
    label.pack(pady=10)

    # Add input fields for name and description
    name_label = tk.Label(root, text="Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=5)

    description_label = tk.Label(root, text="Description:")
    description_label.pack(pady=5)
    description_entry = tk.Entry(root, width=30)
    description_entry.pack(pady=5)

    # Add a button to upload a file
    def handle_upload():
      name = name_entry.get().strip()
      description = description_entry.get().strip()
      if not name or not description:
        messagebox.showerror("Error", "Please fill in both Name and Description fields!")
        return
      file_path = upload_file()
      if file_path:
        convert_into_kml(extract_adif_kml(file_path), name, description)
        messagebox.showinfo("Success", "KML file has been created successfully!")

    upload_button = tk.Button(root, text="Upload File", command=handle_upload)
    upload_button.pack(pady=10)

    # Add an exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    render_window()
