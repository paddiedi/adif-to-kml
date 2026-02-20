from coords import maidenhead_transform
from coords import parse_deg_min
def cdata_format(kml_entry, format, chosen_entries):
    #print(kml_entry)
    try:
        cdata = """"""
        for key, value in format.items():
            cdata += f"{value}: {kml_entry[key]}</br>\n"
        return cdata[:-6] # -6 removing the last </br>.
    except Exception as error:
        #print("KML_BUILD formatting error: ", error)
        pass
    # Formatting will always bypass the chosen entries. If one wants
    # the data formatted, then they should just edit cdata_format.json file.
    # Attempt to create cdata without using the specified formatting:
    cdata = """"""
    for key in chosen_entries:
        if key in kml_entry:
          cdata += f"{key}: {kml_entry[key]}<br>\n"
    return cdata[:-6]

def convert_into_kml(filename, kml_name, kml_description, records, alias, custom_format, chosen_entries, kml_template, skip_on_null_coords):
    format = custom_format
    GRIDSQUARE_ALIAS = alias["GRIDSQUARE_ALIAS"]
    CALL_ALIAS = alias["CALL_ALIAS"]
    LAT_ALIAS = alias["LAT_ALIAS"]
    LON_ALIAS = alias["LON_ALIAS"]
    with open(filename, "w") as output_file:
        output_file.write(kml_template["START"].format(name=kml_name, description=kml_description))
        
        for kml_entry in records:
            cdata = cdata_format(kml_entry, format, chosen_entries) # Custom data, eg. everything else except coordinates etc.
            if alias["LAT_ALIAS"] in kml_entry and alias["LON_ALIAS"] in kml_entry:
                coords = (parse_deg_min(kml_entry[LON_ALIAS]), parse_deg_min(kml_entry[LAT_ALIAS])) # Third coord is altitude?
            elif GRIDSQUARE_ALIAS in kml_entry:
                coords = maidenhead_transform(kml_entry[GRIDSQUARE_ALIAS])
            else:
                if CALL_ALIAS in kml_entry:
                  print(f"Did not find coordinates for: {kml_entry[CALL_ALIAS]}")
                print("Did not find callsign, or any coordinates. Using (0,0)/skipping.")
                coords = (0,0)
            if coords == (0,0) and skip_on_null_coords == "True":
                continue
            
            output_file.write(kml_template["PLACEMARK"].format(cdata=cdata, coord1=coords[0], coord2=coords[1], call=kml_entry[CALL_ALIAS]))
        output_file.write(kml_template["KML_END"])