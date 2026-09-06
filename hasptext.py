######*******************************
###### IDENTIFICATION DIVISION.
######*******************************
###### PROGRAM-ID. HASPTEXT.
###### AUTHOR. ABCPEA.
###### DATE-WRITTEN. 2026-09-04.
######*
######*******************************
###### DATA DIVISION.
######*******************************
###### LINKAGE SECTION.
import argparse

###### WORKING-STORAGE SECTION.
NUM_ROWS    = 12
ROW_WIDTH   = 12
CHAR_WIDTH  = 14
BLOCK_TABLE = {
    "A" : bytearray.fromhex("7FE0FFF0C030C030C030FFF0FFF0C030C030C030C030C030"),
    "B" : bytearray.fromhex("FFE0FFF0C030C030C060FFC0FFC0C060C030C030FFF0FFE0"),
    "C" : bytearray.fromhex("7FE0FFF0C030C000C000C000C000C000C000C030FFF07FE0"),
    "D" : bytearray.fromhex("FF80FFC0C060C030C030C030C030C030C030C060FFC0FF80"),
    "E" : bytearray.fromhex("FFF0FFF0C000C000C000FF00FF00C000C000C000FFF0FFF0"),
    "F" : bytearray.fromhex("FFF0FFF0C000C000C000FF00FF00C000C000C000C000C000"),
    "G" : bytearray.fromhex("7FE0FFF0C030C000C000C000C1F0C1F0C030C030FFF07FE0"),
    "H" : bytearray.fromhex("C030C030C030C030C030FFF0FFF0C030C030C030C030C030"),
    "I" : bytearray.fromhex("7FE07FE0060006000600060006000600060006007FE07FE0"),
    "J" : bytearray.fromhex("3FF03FF0030003000300030003000300C300C300FF007E00"),
    "K" : bytearray.fromhex("C030C060C0C0C180C300FE00FE00C300C180C0C0C060C030"),
    "L" : bytearray.fromhex("C000C000C000C000C000C000C000C000C000C000FFF0FFF0"),
    "M" : bytearray.fromhex("C030E070F0F0D9B0CF30C630C030C030C030C030C030C030"),
    "N" : bytearray.fromhex("C030E030F030D830CC30C630C330C1B0C0F0C070C030C010"),
    "O" : bytearray.fromhex("FFF0FFF0C030C030C030C030C030C030C030C030FFF0FFF0"),
    "P" : bytearray.fromhex("FFE0FFF0C030C030C030FFF0FFE0C000C000C000C000C000"),
    "Q" : bytearray.fromhex("7FE0FFF0C030C030C030C030C030C330C1B0C0F0FFE07FB0"),
    "R" : bytearray.fromhex("FFE0FFF0C030C030C030FFF0FFE0C300C180C0C0C060C030"),
    "$" : bytearray.fromhex("06007FE0FFF0C630E6007FC03FE00670C630FFF07FE00600"),
    "S" : bytearray.fromhex("7FE0FFF0C030C000E0007FC03FE000700030C030FFF07FE0"),
    "T" : bytearray.fromhex("FFF0FFF00600060006000600060006000600060006000600"),
    "U" : bytearray.fromhex("C030C030C030C030C030C030C030C030C030C030FFF07FE0"),
    "V" : bytearray.fromhex("C030C030C030C030C030C030C030606030C019800F000600"),
    "W" : bytearray.fromhex("C030C030C030C030C030C030C630CF30D9B0F0F0E070C030"),
    "X" : bytearray.fromhex("C030C030606030C019800F000F00198030C06060C030C030"),
    "Y" : bytearray.fromhex("C030C030606030C019800F00060006000600060006000600"),
    "Z" : bytearray.fromhex("FFF0FFF0006000C001801FC01FC00C00180030007FF0FFF0"),
    "0" : bytearray.fromhex("3FC07FE0C0F0C1B0C330C630CC30D830F030E0307FE03FC0"),
    "1" : bytearray.fromhex("06000E001E0006000600060006000600060006007FE07FE0"),
    "2" : bytearray.fromhex("7FE0FFF0C0300030003000600180060018006000FFF0FFF0"),
    "3" : bytearray.fromhex("7FE0FFF0C0300030003001E001E000300030C030FFF07FE0"),
    "4" : bytearray.fromhex("038007800D80198031807FF0FFF001800180018001800180"),
    "5" : bytearray.fromhex("FFF0FFF0C000C000C000FF80FFC0006000300030FFF0FFE0"),
    "6" : bytearray.fromhex("7FE0FFF0C030C000C000FFE0FFF0C030C030C030FFF07FE0"),
    "7" : bytearray.fromhex("FFF0FFE0C0C0018003000600060006000600060006000600"),
    "8" : bytearray.fromhex("7FE0FFF0C030C03060603FC03FC06060C030C030FFF07FE0"),
    "9" : bytearray.fromhex("7FE0FFF0C030C030C030FFF0FFF000300030C030FFF07FE0"),
    "#" : bytearray.fromhex("30C030C0FFF0FFF030C030C030C030C0FFF0FFF030C030C0"),
    "@" : bytearray.fromhex("3FC07FE0C030003000301E303F306330C330C3307FE03FC0")}

######*******************************
###### PROCEDURE DIVISION.
######*******************************
def parseArgs():
    parser = argparse.ArgumentParser(
        prog='hasptext',
        description='Convert text to IBM mainframe-style banner')

    parser.add_argument('text', help='The text to be converted')
    parser.add_argument('-c', action='store_true', help='Use centre justification')
    parser.add_argument('-i', action='store_true', help='Use italics')
    parser.add_argument('-w', metavar='WIDTH', default=132, type=int,
                        help='Width of output in columns')

    return parser.parse_args()


def printFill(fill):
    print(f'{'': <{fill}}', end='')


def grabWord(char, row):
    offset  = 2 * row
    hi      = BLOCK_TABLE[char][offset]
    lo      = BLOCK_TABLE[char][offset + 1]

    return (hi << 8) | lo


def printCharRow(char, row):
    word = grabWord(char, row)
    bitmask = 0x8000

    for bit in range(ROW_WIDTH):
        if word & bitmask:
            print(char, end='')
        else:
            print(' ', end='')

        bitmask = bitmask >> 1


def printBlock(text):
    for row in range(ROW_WIDTH):
        printFill(padding)

        if args.i:
            indent = ROW_WIDTH - row
            printFill(indent)

        for char in text:
            if char in BLOCK_TABLE:
                printCharRow(char, row)
                printFill(2)
            elif char == ' ':
                printFill(CHAR_WIDTH)

        print()


def calcPadding(maxLength, length):
    return max(0, (maxLength - length) * CHAR_WIDTH / 2)


def createTextList(text, maxChars):
    textList    = [""]
    words       = text.split()

    for word in words:
        newEntry = (textList[-1] + ' ' + word).lstrip()

        if len(newEntry) < maxChars:
            textList[-1] = newEntry
        else:
            textList.append(word[:maxChars])

        if len(word) > maxChars:
            textList.append(word[maxChars:])

    return textList


######*******************************
###### MAIN.
######*******************************
args        = parseArgs()
isCentred   = args.c
isItalic    = args.i
width       = args.w
maxChars    = int(width / CHAR_WIDTH)

if isItalic:
    maxChars -= 1

textList    = createTextList(args.text.upper(), maxChars)
padding     = 0

for text in textList:
    if isCentred:
        padding = calcPadding(maxChars, len(text))

    printBlock(text)
    print()