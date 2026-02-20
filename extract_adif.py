DEFAULT_ID_LIST = [
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
from ftfy import fix_encoding
def legacy_gen_adif_dictionary(file_path):
   id_dict = []
   with open(file_path, encoding="utf-8") as adif_input_file:
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

class adif_parser():
    def __init__(self, filepath, use_ftfy):
      self.filepath = filepath
      self.use_ftfy = use_ftfy
      self.records = []
      # Line by line parser, also way more efficient when using __iter__ / yield!
    def __iter__(self):
        record_start = False
        with open(self.filepath, encoding="utf-8") as adif_file:
            temp = {}
            for line in adif_file:
                #print(line)
                line_data = line.strip()
                if self.use_ftfy == "True":
                    line_data = fix_encoding(line_data)
                # One does not know how the file is structured.
                # In the future tho might add a checker.
                # This is the "safest" way (slowest).
                if line_data.upper() == "<EOH>":
                    record_start = True
                    continue
                if line_data.upper() == "<EOR>":
                    if temp:
                        yield temp
                    temp = {}
                    continue
                if record_start:
                    if line_data.strip() == "":
                        continue # Skips every empty spot
                    start_index = line_data.index(">")
                    name = ''.join(filter(lambda z: not z.isdigit(), line_data[0:start_index])).replace(":", "").replace("<", "")
                    if not (name in self.records):
                        self.records.append(name) # User can select which records to keep etc.
                    temp[name] = line_data[(start_index+1):]
    # Older method. Made to check when the entries are all on 1 line. (in the official format this aint the case...)
    # Didn't know that back then when I made this. Worked for the file I used which was enough!
    @staticmethod
    def legacy_extract_adif_kml(file_path, use_defaults, **kwargs):
        with open(file_path, encoding="utf-8") as adif_input_file:
            data = []
            if use_defaults:
                entry_id_list = DEFAULT_ID_LIST
                print("Using default ADIF config")
            else:
                entry_id_list = kwargs.get("entry_id_list", None)
            for line in adif_input_file:
                entry_dictionary = {key: "" for key in entry_id_list}
                entries = line.split()
                for i in entries:
                    for name in entry_id_list:
                        stripped = i.strip()
                        if stripped.startswith(f"<{name}:"):
                            # Look for where the > char is, also this looks like spagetti :/
                            start_index = stripped.index(">")
                            entry_dictionary[name] = stripped[(start_index + 1):]
                        else:
                            pass
                data.append(entry_dictionary)
            return data
    
if __name__ == "__main__":
    data = []
    parser = adif_parser("kusot.adi", "")
    for record in parser:
        data.append(record)
    print(parser.records)
