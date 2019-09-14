""" Parses raw data from some external source """
import point


# I hope these are consistant across devices
EVENT_TYPE_ABS = 3
EVENT_CODE_X = 0
EVENT_CODE_Y = 1

EVENT_TYPE_SYN = 0
EVENT_CODE_REPORT = 0




def parse_file(file_handle):
    """ Parses the otput from an evemu recording. This recording
    can be made using `evemu-record > output.data`. You can trim it
    with a texty editor to only include interesting parts.
    I haven't tested this across multiple devices, so hopefully it
    works adequatly.

    It's worth mentioning that this software (as a whole) does not
    support encoding pen up/down data.
    """
    points = []

    x = 0
    y = 0
    for line in file_handle.readlines():
        if line[0] != 'E':
            # We only care about events
            continue
        data = line.split()

        e_type = int(data[2], 16)
        e_code = int(data[3], 16)
        e_data = int(data[4])


        if e_type == EVENT_TYPE_ABS:
            if e_code == EVENT_CODE_X:
                x = e_data
            if e_code == EVENT_CODE_Y:
                y = -e_data

        if e_type == EVENT_TYPE_SYN and e_code == EVENT_CODE_REPORT:
            if x != 0 and y != 0:
                points.append(point.Point(x, y))
    return points
