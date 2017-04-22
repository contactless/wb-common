from __future__ import print_function
import re
import os

# get_mac() has been moved to test_suite, because it uses wb-gen-serial,
# which depends on this (wb-common) package (avoid circular dependency)


def get_cpuinfo_serial():
    data = open('/proc/cpuinfo').read()
    matches = re.findall('^Serial\s+: ([0-9a-f]+)$', data, re.M)
    if len(matches) > 0:
        return matches[0]
    return None


def get_mmc_serial():
    mmc_prefix = '/sys/class/mmc_host/mmc0/'
    if os.path.exists(mmc_prefix):
        for entry in os.listdir(mmc_prefix):
            if entry.startswith('mmc'):
                serial_fname = mmc_prefix + entry + '/serial'
                if os.path.exists(serial_fname):
                    serial = open(serial_fname).read().strip()
                    if serial.startswith('0x'):
                        serial = serial[2:]
                    return serial
    return None

def get_eeprom_serial(num = 0):
    if num == 0:
        eeprom = "4-0057"
    elif num == 1:
        eeprom = "5-0057"
    eeprom = "/sys/bus/i2c/devices/" + eeprom + "/eeprom"

    if os.path.exists(eeprom):
        mac = bytearray(open(eeprom).read(256)[250:])
        return ''.join(map(lambda b: format(b, "02x"), mac))

    return None


if __name__ == '__main__':
    print("/proc/cpuinfo serial: ", get_cpuinfo_serial())
    #print "WB serial (eth mac): ", get_mac()
