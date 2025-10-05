
# 1. Field A-R
# 2. Square 0-9
# 3. Subsquare a-x
# 4. Extended square 0-9
# 5. Extended subsquare a-x
# ...
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def calc_coords(maiden_string: str):
    '''
    Translates maiden coordinates into longitude/latitude
    E/N (east, north) form.
    '''
    #print(maiden_string)
    if maiden_string == "":
        #print("WARNING MAIDENHEAD NOT DEFINED, RETURNING (0,0)")
        return (0,0)
    # Init longitude and latitude ranges
    longitude_init = -180+(ALPHABET.index(maiden_string[0].upper()))*20
    latitude_init = -90+ALPHABET.index(maiden_string[1].upper())*10

    trimmed_maiden = maiden_string[2:]
    longitude_calc_string = trimmed_maiden[::2]
    latitude_calc_string = trimmed_maiden[1::2]

    def calc_range(calc_string, range_len, start):
        index = 0
        for char in calc_string:
            if index % 2 == 0:
                increment = range_len / 10
                start += int(char) * increment

            else:
                increment = range_len / 24
                start += increment*(ALPHABET.index(char.upper()))
            index += 1
            range_len = increment
        return (start, start+range_len)

    range_len_longitude = 20
    range_len_latitude = 10

    longitude = calc_range(longitude_calc_string, range_len_longitude, longitude_init)
    latitude = calc_range(latitude_calc_string, range_len_latitude, latitude_init)
    # Because the wanted coordinate is NOT in a range, the coordinate shall
    # be a middle ground. Thus:
    longitude = longitude[0]+(longitude[1]-longitude[0])/2
    latitude = latitude[0]+(latitude[1]-latitude[0])/2
    return (longitude, latitude)