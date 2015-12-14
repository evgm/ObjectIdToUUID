import datetime as dt
from bson import ObjectId
from uuid import UUID


class UTC(dt.tzinfo):
    ZERO = dt.timedelta(0)

    def utcoffset(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return self.ZERO

UTC = UTC()
UUID_1_EPOCH = dt.datetime(1582, 10, 15, tzinfo=UTC)
UUID_TICKS_PER_SECOND = 10000000


def unix_time_to_uuid_time(dt):
    return int((dt - UUID_1_EPOCH).total_seconds() * UUID_TICKS_PER_SECOND)


def object_id_to_uuid(object_id):
    """
    Converts ObjectId to UUID

    :param object_id: some ObjectId
    :return: UUID
    """

    str_object_id = str(object_id)

    b = []
    for i in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]:
        b.append(int(str_object_id[i:i+2], 16))

    generation_time = ObjectId(str_object_id).generation_time.astimezone(UTC)
    time = unix_time_to_uuid_time(generation_time)
    time |= (b[4] >> 6) & 0x3

    most_sig_bits = str(hex(0x1000 | time >> 48 & 0x0FFF
                            | time >> 16 & 0xFFFF0000
                            | time << 32))[9:]

    least_sig_bits = str(hex(2 << 62
                             | (b[4] & 0x3F) << 56 | (b[5] & 0xFF) << 48
                             | (b[6] & 0xFF) << 40 | (b[7] & 0xFF) << 32
                             | (b[8] & 0xFF) << 24 | (b[9] & 0xFF) << 16
                             | (b[10] & 0xFF) << 8 | b[11] & 0xFF))[2:]

    return UUID('%s-%s-%s-%s-%s' % (most_sig_bits[:8], most_sig_bits[8:12], most_sig_bits[12:16],
                               least_sig_bits[0:4], least_sig_bits[4:]))