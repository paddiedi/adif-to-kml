import tkinter as tk
from tkinter import filedialog, messagebox
from kmlbuild import convert_into_kml
import extract_adif
import sys
import yaml
DEFAULT_OUTPUT_FILE="output.kml"
#with open("aliases.json") as alias_file:
   #ALIASES = json.load(alias_file)
def get_settings():
   with open("settings.yaml", encoding="utf-8") as settings_file:
    try:
      data = yaml.safe_load(settings_file)
      #print(data)
    except Exception:
        raise "Could not find settings file!"
    print("Settings found!")
    return data
SETTINGS = get_settings()
def upload_file():
    filepath = filedialog.askopenfilename(title="Select a File")
    if filepath:
        messagebox.showinfo("File Selected", f"You selected: {filepath}")
        return filepath
    return None

def main():
    root = tk.Tk()
    root.title("ADIF-KML CONVERTER")
    root.geometry("600x400")

    label = tk.Label(root, text="ADIF-KML CONVERTER", font=("Arial", 14))
    label.pack(pady=10)

    name_label = tk.Label(root, text="KML title:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root, width=30)
    name_entry.pack(pady=5)

    description_label = tk.Label(root, text="KML description:")
    description_label.pack(pady=5)
    description_entry = tk.Entry(root, width=30)
    description_entry.pack(pady=5)

    file_name_label = tk.Label(root, text="Filename (optional):")
    file_name_label.pack(pady=5)
    file_name_entry = tk.Entry(root, width=30)
    file_name_entry.pack(pady=5)

    use_defaults_var = tk.BooleanVar()
    defaults_checkbox = tk.Checkbutton(
        root, text="Use default values", variable=use_defaults_var
    )
    defaults_checkbox.pack(pady=5)

    def select_options(options):
      window = tk.Toplevel()
      window.geometry("600x400")
      window.title("Select ADIF-entries")

      # Create a frame for the canvas and scrollbar
      frame = tk.Frame(window)
      frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

      canvas = tk.Canvas(frame)
      canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

      scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
      scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

      scroll_frame = tk.Frame(canvas)
      scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
      )
      canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
      canvas.configure(yscrollcommand=scrollbar.set)

      # Create checkboxes
      checkbox_vars = {}
      for val in options:
        var = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(scroll_frame, text=val, variable=var)
        checkbox.pack(anchor="w", padx=5, pady=2)
        checkbox_vars[val] = var

      selected = []

      def on_ok():
        nonlocal selected
        selected = [k for k, v in checkbox_vars.items() if v.get()]
        window.destroy()

      button_frame = tk.Frame(window)
      button_frame.pack(fill=tk.X, padx=10, pady=10)

      ok_button = tk.Button(button_frame, text="Confirm", command=on_ok)
      ok_button.pack(side=tk.RIGHT)

      window.wait_window()
      return selected
    def exit():
       root.quit()
       root.destroy()
       sys.exit()

    def handle_upload():
      try:

        name = name_entry.get().strip()
        description = description_entry.get().strip()
        use_defaults = use_defaults_var.get()
        filename = file_name_entry.get().strip()
        if filename == "" or filename == None:
           filename = SETTINGS["OUTPUT_FILE"]
        if not name or not description:
          messagebox.showerror("Error", "Please fill in both Name and Description fields!")
          return
        filepath = upload_file()
        if filepath:
          # Parse the adif file for all the entries
          # Also using ftfy to fix some unicode errors :)
          adif_parser = extract_adif.adif_parser(filepath, SETTINGS["USE_FTFY"])
          custom_format = SETTINGS["DEFAULT_FORMAT"]
          data = [record for record in adif_parser]
          record_ids = adif_parser.records
          #print(SETTINGS["ALIASES"])
          #print(record_ids)
          entry_id_list = []
          if not use_defaults:
            entry_id_list = select_options(record_ids)
            custom_format = SETTINGS["CDATA_FORMAT"]

          convert_into_kml(
              filename,
              name,
              description,
              data,
              alias=SETTINGS["ALIASES"],
              custom_format=custom_format,
              chosen_entries=entry_id_list,
              kml_template={
                  "START": SETTINGS["KML_START_TEMPLATE"],
                  "KML_END": SETTINGS["KML_END_TEMPLATE"],
                  "PLACEMARK": SETTINGS["KML_PLACEMARK_TEMPLATE"],
                  "SIMPLEDATA": SETTINGS["KML_SIMPLEDATA"],
              }, skip_on_null_coords=SETTINGS["SKIP_ON_NULL_COORDS"]
          )
          messagebox.showinfo(message=f"Conversion succesful, open {filename} to see the result.", title="Conversion success")
          exit()
      except Exception as error:
         messagebox.showerror(title="Crash report", message=error)
         exit()
    upload_button = tk.Button(root, text="Upload File", command=handle_upload)
    upload_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=15, height=2)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
