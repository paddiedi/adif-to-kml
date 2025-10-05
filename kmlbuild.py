KML_START_TEMPLATE = \
"""<?xml version="1.0" encoding="UTF-8"?>
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
    </Style>
"""
KML_END_TEMPLATE = \
"""\n</Document>\n</kml>
"""
KML_PLACEMARK_TEMPLATE = \
"""
<Placemark>
  <name>{call}</name>
  <description>
    <![CDATA[\n{cdata}
    ]]>
  </description>
  <Point>
    <coordinates>{coord1},{coord2},0</coordinates>
  </Point>
</Placemark>
"""
DEFAULT_FORMAT = {
    "QSO_DATE": "QSO Date",
    "TIME_ON": "Time On",
    "TIME_OFF": "Time Off",
    "BAND": "Band",
    "FREQ": "Frequency",
    "MODE": "Mode",
    "RST_RCVD": "RST Received",
    "TX_PWR": "Power",
    "OPERATOR": "Operator",
    "CONTEST_ID": "Contest",
    "CQZ": "CQ Zone"
}
from grid import calc_coords

def cdata_format(kml_entries, format):

    cdata = """"""
    for key, value in format.items():
        cdata += f"{value}: {kml_entries[key]}</br>\n"
    return cdata[:-6] # -6 removing the last </br>.

def convert_into_kml(filename, kml_name, kml_description, kml_entries, use_defaults, **kwargs):

    if use_defaults:
        print("Using default CDATA-format")
        format = DEFAULT_FORMAT
    else:
        format = kwargs.get("format", None)
    print(format)
    with open(filename, "w") as output_file:
        output_file.write(KML_START_TEMPLATE.format(name=kml_name, description=kml_description))
        
        for kml_entry in kml_entries:
            cdata = cdata_format(kml_entry, format)
            coords = calc_coords(kml_entry["GRIDSQUARE"])
            output_file.write(KML_PLACEMARK_TEMPLATE.format(cdata=cdata, coord1=coords[0], coord2=coords[1], call=kml_entry["CALL"]))
        output_file.write(KML_END_TEMPLATE)
        # Oletan että GRIDSQUARE ja CALL nimet eivät muutu historian saatossa :D