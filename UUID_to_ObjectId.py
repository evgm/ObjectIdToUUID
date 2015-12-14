import datetime as dt
from bson import ObjectId
import pytz


def get_timestamp_from_uuid(uuid_object):

    generation_time = dt.datetime.utcfromtimestamp((uuid_object.time - 0x01b21dd213814000) * 100 / 1e9)
    generation_time = generation_time.replace(tzinfo=pytz.UTC)

    return int(generation_time.timestamp())


def get_timestamp_from_object_id(object_id):

    generation_time = object_id.generation_time
    return int(generation_time.timestamp())


def return_decimal_bytes(binary):

    binary = binary[2:]
    rest = len(binary) % 8

    if rest != 0:
        binary = '0'*(8 - rest) + binary
    bytes = {}

    for i in range(0, len(binary)//8):
        bytes[i] = binary[:8]
        binary = binary[8:]

    return bytes


def uuid_to_object_id(uuid_object):
    """
    Converts UUID to ObjectId

    :param uuid_object: UUID
    :return: ObjectId
    """

    uuid_to_bin = bin(int(uuid_object))
    parts_of_uuid = return_decimal_bytes(uuid_to_bin)

    timestamp_of_uuid = hex(get_timestamp_from_uuid(uuid_object))
    timestamp_of_uuid = timestamp_of_uuid.replace('0x', '')

    uuid_time = uuid_object.time

    fourth = int(parts_of_uuid[8], 2) & 0x3F | (uuid_time << 6)
    fourth = str(hex(fourth))[-2:]

    fifth = str(hex(int(parts_of_uuid[9], 2)))
    sixth = str(hex(int(parts_of_uuid[10], 2)))
    seventh = str(hex(int(parts_of_uuid[11], 2)))
    eighth = str(hex(int(parts_of_uuid[12], 2)))
    ninth = str(hex(int(parts_of_uuid[13], 2)))
    tenth = str(hex(int(parts_of_uuid[14], 2)))

    try:
        eleventh = str(hex(int(parts_of_uuid[15], 2)))
    except Exception as e:
        print(e)
        eleventh = str(hex(1))

    def rep(el):
        if len(el) <= 3:
            return el.replace('x', '')
        else:
            return el.replace('0x', '')

    res = rep(fifth) + rep(sixth) + rep(seventh) + rep(eighth) + rep(ninth) + rep(tenth) + rep(eleventh)

    return ObjectId(timestamp_of_uuid + fourth + res)



