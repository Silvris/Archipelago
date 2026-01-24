try:
    from calculate_crc import recalculate_6103_crcs
except ImportError:
    from ..calculate_crc import recalculate_6103_crcs  # if running from /src/ directory

def recalc_basepatch_crc():
    file = open("K64Basepatch.z64", 'rb')
    data = file.read()

    data = recalculate_6103_crcs(data)

    file = open("K64Basepatch.z64", 'wb')
    file.write(data)

recalc_basepatch_crc()