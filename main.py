import tkinter as tk
from tkinter import filedialog, messagebox
from kmlbuild import convert_into_kml
from extract_adif import extract_adif_kml
from extract_adif import gen_adif_dictionary
import sys
import json

def upload_file():
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        messagebox.showinfo("File Selected", f"You selected: {file_path}")
        return file_path
    return None

def render_window():
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
    # On exceptions, call this command
    def handle_upload():
      name = name_entry.get().strip()
      description = description_entry.get().strip()
      use_defaults = use_defaults_var.get()
      filename = file_name_entry.get().strip()
      if filename == "" or not filename:
         filename == "output.kml"
      if not name or not description:
        messagebox.showerror("Error", "Please fill in both Name and Description fields!")
        return
      file_path = upload_file()
      if file_path:
        if use_defaults:
          convert_into_kml(filename, name, description, extract_adif_kml(file_path, use_defaults), use_defaults)
        else:
           entry_dictionary_id = select_options(gen_adif_dictionary(file_path))
           try:
              with open("cdata_format.json", "r") as kml_format_file:
                kml_format = json.load(kml_format_file)
           except FileNotFoundError:
              messagebox.showerror("KML_format json file not found, exiting...")
              exit()

           #print(entry_dictionary_id)
           if "CALL" not in entry_dictionary_id or "GRIDSQUARE" not in entry_dictionary_id:
              print("Error", "You dummy, why did you take CALL and GRIDSQUARE off :D Now exiting...")
              exit()
           else:
              convert_into_kml(filename, name, description, extract_adif_kml(file_path, use_defaults, entry_dictionary_id=entry_dictionary_id), use_defaults, format=kml_format)
           messagebox.showinfo(message=f"Conversion succesful, open {filename} to see the result.", title="Conversion success")
           exit()
    upload_button = tk.Button(root, text="Upload File", command=handle_upload)
    upload_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=15, height=2)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    render_window()
