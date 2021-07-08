# this is for making the functions for converting a floating point to binary. 
import math, struct

## CONVERTS DECIMAL TO BINARY
###############################################
def IEEE(num):
    # convert to binary using IEEE 754
    print("decimal to binary")
    sign = ""
    exponent = 0
    mantissa = ''
    bin = ''

    # find the sign bit
    if num < 0:
        sign += "1"
    else:
        sign += "0"

    # find the representation in base-2 scientific notation
    # lets seperate the left of the decimal and the right of the decimal.
    # lets find the location of the decimal
    loc = 0
    for i in range(len(str(num))):
        if str(num)[i] == ".":
            loc = i
    whole = str(num)[0:loc]
    fraction = str(num)[loc+1:len(str(num))]

    # get the binary of the whole number
    whole_bin = ""
    eq = 1
    while eq != 0:
        eq = int(int(whole) / 2)
        whole_bin = str(int(whole) % 2) + whole_bin
        whole = eq

    # get the binary of the fraction
    fraction_bin = ""
    fraction = float("0." + fraction)
    count = 0
    stuff = fraction
    while stuff != 0 and count < 52:
        print(stuff)
        stuff = fraction * 2
        fraction_bin = fraction_bin + str(stuff)[0]
        fraction = float(str(stuff)[1:len(str(stuff))])
        count +=1 
        if stuff == 0:
            print("actually exited")
    print("fraction binary:", fraction_bin)                     # this seems to be right


    # getting the scientific notation... this way we can see what the exponent has to be
    string = "{:e}".format(float(whole_bin + "." + fraction_bin))
    val = ''
    for i in range(4,-1, -1):
        if string[len(string)-1-i] != "e":
            val += string[len(string)-1-i]
        if string[len(string)-1-i] == "e":
            val = ""

    print(int(val))
    mantissa = whole_bin[len(whole_bin)-int(val):len(whole_bin)] + fraction_bin
    print(mantissa)
    exponent = int(val) + 1023

    # put the exponent into binary
    exponent_bin = ""
    val = 1
    while val != 0:
        val = int(exponent / 2)
        exponent_bin = str(exponent%2) + exponent_bin
        exponent = val
    exponent_bin = exponent_bin.zfill(11)
    bin = sign + " " + exponent_bin + " " + mantissa.ljust(52, "0")

    # return the value
    return bin


## here is where the code will run
##################################
def main():
    # print(IEEE(10.25))
    # print(IEEE(774.241638183594))
    f = 1.2717441261e+20
    print (str(struct.pack("f", f)).encode("hex"))
    # print (''.join("%x" % ord(c) for c in struct.unpack(">8c", buf) ))

if __name__ == '__main__':
    main()