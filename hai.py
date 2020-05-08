#!/usr/bin/python

import sys
import re
import binascii


test_hex_1 = "0x41 0x42 0x43"
test_hex_2 = "0x414243"
test_hex_3 = "\\x41\\x42\\x43"
test_hex_4 = "x41 x42 x43"
test_hex_5 = "414243"

#FORMAT_DEFAULT = '\x5Cx{}'
FORMAT_DEFAULT = '\\x{}'
#FORMAT_DEFAULT = '0x{} '

rx_numbers = r'^[0-9]+$'
rx_hex = r'^(0x|x|\\x)?([0-9a-fA-F]{2,}$)'
rx_hex_pairs = r'^(\\x[0-9a-fA-F]{2}\s?)+$'





def characterize_data(data_string):
    """
    Input will be a string from command-line need to figure out the format (best guess)
    """
    out_int = []
    #out_hex = []
    out_hex = ""
    out_ascii = []

    # Split on spaces
    data_split = data_string.split()
    if len(data_split) == 1:
        # Only on continous string, no spaces...
        print(data_split[0])

        # Check if only integers
        mtch = re.match(rx_numbers, data_split[0])
        if mtch:
            # This is most likely an integer
            data_int = int(data_string)
            print("Integer?")
            print(data_int)
            hex_str = hex(data_int)[2:]
            if len(hex_str) % 2:
                hex_str = "0" + hex_str
            #print(hex(data_int))
            unhex = binascii.unhexlify(hex_str)
            for i in unhex:
                value_int = ord(i)
                out_int.append(value_int)
                out_hex = out_hex + FORMAT_DEFAULT.format(hex(value_int)[2:])
            print(out_hex)
            #print(hex_str)
            print(unhex)
            return

        # Single hex value
        mtch = re.match(rx_hex, data_split[0])
        if mtch:
            print("Hex?")
            value = mtch.group(2)
            print(value)
            unhex = binascii.unhexlify(value)
            if len(unhex) == 1:
                value_int = ord(unhex)
                print(value_int)
                print(FORMAT_DEFAULT.format(hex(value_int)[2:]))
                print(unhex)
            else:
                for i in unhex:
                    value_int = ord(i)
                    out_int.append(value_int)
                    out_hex = out_hex + FORMAT_DEFAULT.format(hex(value_int)[2:])
                print(out_int)
                print(out_hex)
                print(unhex)
            return

        # Repeated hex
        mtch = re.match(rx_hex_pairs, data_split[0])
        if mtch:
            v_split = mtch.group(0).split('\\x')
            value = ''.join(v_split)
            unhex = binascii.unhexlify(value)
            for i in unhex:
                value_int = ord(i)
                out_int.append(value_int)
                #out_hex.append('\x5C' + hex(value_int)[1:])
                out_hex = out_hex + '\x5C' + hex(value_int)[1:]
            print(out_int)
            print(out_hex)
            print(unhex)
            return

        else:
            print("Byte array?")
            ba = bytearray(data_split[0])
            for i in ba:
                out_int.append(i)
                #out_hex.append(hex(i))
                out_hex = out_hex + '\x5C' + hex(i)[1:]
                out_ascii.append(chr(i))
            print(out_int)
            print(out_hex)
            print(out_ascii)

            #print("No match")



def main(argv):
    rx_hex = r'^(0x|x|\\x)([0-9a-f]{2}$)'
    rx_int = r'[0-9]+'

    if len(argv) != 2:
        print("Only one arg accepted")
        return

    mode = argv[0]
    if mode not in ('h', 'a', 'i'):
        print("Unsupported mode")
        return

    value = argv[1]
    
    out_ascii = []
    out_int = []
    out_hex = []

    if mode == 'h':
        char_array = value.split()
        for c in char_array:
            match = re.match(rx_hex, c)
            if match:
                value = match.group(2)
                value_int = ord(binascii.unhexlify(value))
                out_int.append(value_int)
                out_hex.append(hex(value_int))
                out_ascii.append(chr(value_int))

    if mode == 'a':
        for c in value:
            value_int = ord(c)
            out_int.append(value_int)
            out_hex.append(hex(value_int))
            out_ascii.append(chr(value_int))

    if mode == 'i':
        int_array = value.split()
        for s in int_array:
            value_int = int(s)
            out_int.append(value_int)
            out_hex.append(hex(value_int))
            out_ascii.append(chr(value_int))

    print(out_int)
    print(out_hex)
    print(out_ascii)




if __name__ == "__main__":
    #main(sys.argv[1:])
    characterize_data(sys.argv[1])
