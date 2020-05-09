#!/usr/bin/python

import sys
import re
import binascii

test_hex_1 = "0x41 0x42 0x43"
test_hex_4 = "x41 x42 x43"
test_hex_2 = "0x414243"
test_hex_3 = "\\x41\\x42\\x43"
test_hex_5 = "414243"

FORMAT_DEFAULT = '\\x{}'
# Other format -> FORMAT_DEFAULT = '0x{} '

rx_numbers = r'^[0-9]+$'
rx_hex = r'^(0x|x|\\x)?([0-9a-fA-F]{2,}$)'
rx_hex_pairs = r'^(\\x[0-9a-fA-F]{2}\s?)+$'


def print_hai(h, a, i):
    """ Prints out HAI data """
    print("Hex:     {}".format(h))
    print("Ascii:   {}".format(a))
    print("Int:     {}".format(i))


def hex_to_pretty(hex_str, hex_format=FORMAT_DEFAULT):
    """
    Take a hex string like '31324a4b' and turns it into a formatted version
    like '\\x31\\x32\\x4a\\x4b' or what ever FORMAT is specified
    """
    out_hex = ""
    out_int = []
    out_ascii = ""

    unhex = binascii.unhexlify(hex_str)
    out_ascii = unhex
    if len(unhex) == 1:
        v_int = ord(unhex)
        out_hex = hex_format.format(hex(v_int)[2:])
        out_int = [v_int]
    else:
        for i in unhex:
            v_int = ord(i)
            out_int.append(v_int)
            out_hex = out_hex + hex_format.format(hex(v_int)[2:])
    return (out_hex, out_ascii, out_int)


def characterize_data(data_string):
    """
    Input will be a string from command-line need to figure out the format (best guess)
    """
    out_int = []
    out_hex = ""
    out_ascii = []

    # Split on spaces
    data_split = data_string.split()
    if len(data_split) == 1:

        # Only integers?
        mtch = re.match(rx_numbers, data_string)
        if mtch:
            print("Input: {} - INT".format(mtch.group(0)))
            data_int = int(data_string)
            hex_str = hex(data_int)[2:]
            if len(hex_str) % 2:
                hex_str = "0" + hex_str
            (h, a, i) = hex_to_pretty(hex_str)
            print_hai(h, a, i)
            return

        # Single hex value?
        mtch = re.match(rx_hex, data_string)
        if mtch:
            print("Input: {} - HEX".format(mtch.group(0)))
            value = mtch.group(2)
            (h, a, i) = hex_to_pretty(value)
            print_hai(h,a,i)
            return

        # Repeated hex value?
        mtch = re.match(rx_hex_pairs, data_string)
        if mtch:
            print("Input: {} - HEX-REPEATED".format(mtch.group(0)))
            v_split = mtch.group(0).split('\\x')
            value = ''.join(v_split)
            (h, a, i) = hex_to_pretty(value)
            print_hai(h, a, i)
            return

        # Something else, maybe byte array?
        else:
            print("Input: {} - BYTE-ARRAY".format(data_string))
            hex_str = binascii.hexlify(data_string)
            (h, a, i) = hex_to_pretty(hex_str)
            print_hai(h, a, i)
            return



if __name__ == "__main__":
    argc = len(sys.argv)
    #main(sys.argv[1:])
    if argc == 1:
        # Read from stdin
        characterize_data(sys.stdin.read())
    else:
        characterize_data(sys.argv[1])
