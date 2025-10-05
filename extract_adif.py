default_dictionary_id = [
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
def gen_adif_dictionary(file_path):
   id_dict = []
   with open(file_path) as adif_input_file:
    for line in adif_input_file:
       entries = line.split()
       stripped = entries[0].strip()
       if not stripped.startswith("<"):
          pass  # Erittäin laiskaa koodii :D
       elif entries[0] == "<EOH>":
          pass
       else:
            for entry in entries[:-1]:
                #print(entry)
                entry = entry[:entry.index(":")]
                entry = entry.strip().replace("<", "").replace(":", "")
                id_dict.append(entry)
            break
    return id_dict

def extract_adif_kml(file_path, use_defaults, **kwargs):
  with open(file_path) as adif_input_file:
    data = []
    if use_defaults:
       entry_dictionary_id = default_dictionary_id
       print("Using default ADIF config")
    else:
       entry_dictionary_id = kwargs.get("entry_dictionary_id", None)
    for line in adif_input_file:
        entry_dictionary = {key: "" for key in entry_dictionary_id}
        entries = line.split()
        for i in entries:
            for name in entry_dictionary_id:
                stripped = i.strip()
                if stripped.startswith(f"<{name}:"):
                    # Look for where the > char is, also this looks like spagetti :/
                    start_index = stripped.index(">")
                    entry_dictionary[name] = stripped[(start_index + 1):]
                else:
                    pass
        data.append(entry_dictionary)
    return data