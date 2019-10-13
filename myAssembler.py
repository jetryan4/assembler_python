#!/usr/bin/env python

#python script for converting assembly to machine code
#Jet Ryan

#this is throughly test for cases:
#   -do not have enough arguements
#   -are not a proper command
#   -reach outside the limit of immediate length
#   -handles items outside the range of a shift amount
#   -handles incorrect registers

#must be placed in a function to call file input name
#and return output

# The program can be simply run by the commandline
# the program needs to be compiled on a linux machine with the command
# $ chmod +x myAssembler.py
# then excuted by:
# $ ./myAssembler.py *.s
# outputs *.obj


import logging
import sys

mips_commands = { # opcode and function
    "add" : ("R", "000000", "100000"), #R type
    "addi" : ("I" ,"001000", "000000"), #I type
    "addiu" : ("I", "001001", "000000"), #I type
    "addu" : ("R", "000000", "100001"), #R type
    "and" : ("R", "000000", "100100"),
    "andi" : ("I", "001100", "000000"),
    "beq" : ("I", "000100", "000000"),
    "bne" : ("I", "000101", "000000"),
    "jr" : ("R", "000000", "001000"),
    "lbu" : ("I", "100100", "000000"),
    "lhu" : ("I", "100101", "000000"),
    "ll" : ("I", "110000", "000000"),
    "lui" : ("I", "001111", "000000"),
    "lw" : ("I", "100011", "000000"),
    "nor" : ("R", "000000", "100111"),
    "or" : ("R", "000000", "100101"),
    "ori" : ("I", "001101", "000000"),
    "slt" : ("R", "000000", "101010"),
    "slti" : ("I", "001010", "000000"),
    "sltu" : ("R", "000000", "101011"),
    "sll" : ("R", "000000", "000000"),
    "srl" : ("R", "000000", "000010"),
    "sb" : ("I", "101000", "000000"),
    "sc" : ("I", "111000", "000000"),
    "sh" : ("I", "101001", "000000"),
    "sw" : ("I", "101011", "000000"),
    "sub" : ("R", "000000", "100010"),
    "subu" : ("R", "000000", "100011")

}

mips_registers = {
    "$zero" : "00000",
    "$at" : "00001",
    "$v0" : "00010",
    "$v1" : "00011",
    "$a0" : "00100",
    "$a1" : "00101",
    "$a2" : "00110",
    "$a3" : "00111",
    "$t0" : "01000",
    "$t1" : "01001",
    "$t2" : "01010",
    "$t3" : "01011",
    "$t4" : "01100",
    "$t5" : "01101",
    "$t6" : "01110",
    "$t7" : "01111",
    "$s0" : "10000",
    "$s1" : "10001",
    "$s2" : "10010",
    "$s3" : "10011",
    "$s4" : "10100",
    "$s5" : "10101",
    "$s6" : "10110",
    "$s7" : "10111",
    "$t8" : "11000",
    "$t9" : "11001",
    "$k0" : "11010",
    "$k1" : "11011",
    "$s7" : "10111",
    "$gp" : "11100",
    "$sp" : "11101",
    "$fp" : "11110",
    "$ra" : "11111",
}

def bdig(n, b):
    s = bin(n & int("1"*b, 2))[2:]
    return ("{0:0>%s}" % (b)).format(s)

def checkreg(reg, key):
    if key in reg.keys():
        return reg[key]
    else:
        print("register not recognized: ", key)
        sys.exit()

def data_convert_mips_line(mips_l, count):
    a = mips_l.split(" ")
    argc = len(a)
    #print(a[0])
    stringR = 'opcodersrtrdshamtfunct'
    stringI = 'opcodersrtimmediate'

    curkey = a[0] #the keyname
    stringR = stringR.replace('opcode', mips_commands[curkey][1])
    stringI = stringI.replace('opcode', mips_commands[curkey][1])

    if mips_commands[a[0]][0] == "R":
        stringR = stringR.replace('funct', mips_commands[curkey][2])
        if a[0] == "jr":
            if argc != 2:
                print('Error, incorrect number of arguments in jr instrunction')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            reg_s =  checkreg(mips_registers, a[1])
            reg_t = "00000"
            reg_d = "00000"
            shamt = "00000"
            #print("I entered jr",a,argc)
            stringR = stringR.replace('rs', reg_s)
            stringR = stringR.replace('rt', reg_t)
            stringR = stringR.replace('rd', reg_d)
            stringR = stringR.replace('shamt', shamt)
        elif a[0] == "srl" or a[0] == "sll":
            if argc != 4:
                print('Error, incorrect number of arguments in shift instruction')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()

            reg_s = "00000"
            reg_t = checkreg(mips_registers, a[2])
            reg_d = checkreg(mips_registers, a[1])
            shamt = bdig(int(a[3]), 5)
            if int(a[3]) >= 32:
                print('Error, size of shift amount')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            #print("I entered srl,sll",a,argc)
            stringR = stringR.replace('rs', reg_s)
            stringR = stringR.replace('rt', reg_t)
            stringR = stringR.replace('rd', reg_d)
            stringR = stringR.replace('shamt', shamt)
        else:
            if argc != 4:
                print('Error, incorrect number of arguments in other R type instruction')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            shamt = "00000"
            reg_s = checkreg(mips_registers, a[2])
            reg_t = checkreg(mips_registers, a[3])
            reg_d = checkreg(mips_registers, a[1])
            #print("I entered all other R commands",a,argc)
            stringR = stringR.replace('rs', reg_s)
            stringR = stringR.replace('rt', reg_t)
            stringR = stringR.replace('rd', reg_d)
            stringR = stringR.replace('shamt', shamt)
        stringR = str('%08X' % int(stringR, 2)).lower()
        return stringR
    elif mips_commands[a[0]][0]  == "I":
        if a[0] == "sw" or a[0] == "lw" or a[0] == "lbu" or a[0] == "lhu" or a[0] == "sb" or a[0] == "sh":
            if argc != 4:
                print('Error, incorrect number of arguments in load or store')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            if int(a[2]) > 32767 or int(a[2]) < -32768:
                print('Error, size of immediate')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            immediate = bdig(int(a[2]), 16)

            reg_s = checkreg(mips_registers, a[3])
            reg_t = checkreg(mips_registers, a[1])
            #print("I entered sw,lw,lbu,lhu,sb,sh",a,argc)
            stringI = stringI.replace('rt', reg_t)
            stringI = stringI.replace('rs', reg_s)
            stringI = stringI.replace('immediate', immediate)
        elif a[0] == "beq" or a[0] == "bne":
            if argc != 4:
                print('Error, incorrect number of arguments in branch')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()
            immediate = bdig(int(a[3]), 16)
            if int(a[3]) > 32767 or int(a[3]) < -32768:
                print('Error, size of immediate')
                print('Cant assemble line number: ')
                print(count + 1)
                print(mips_l)
                sys.exit()

            reg_s = checkreg(mips_registers, a[1])
            reg_t = checkreg(mips_registers, a[2])
            #print("I enter beq,bne",a,argc)
            stringI = stringI.replace('rt', reg_t)
            stringI = stringI.replace('rs', reg_s)
            stringI = stringI.replace('immediate', immediate)
        else:
            if argc != 4:
                print('Error, incorrect number of arguments in other I type instrunction')
                sys.exit()
            immediate = bdig(int(a[3]), 16)
            if curkey == "ori" or curkey == "andi":
                if int(a[3]) >= 65536:
                    print('Error, size of immediate')
                    print('Cant assemble line number: ')
                    print(count + 1)
                    print(mips_l)
                    sys.exit()
            else:
                if int(a[3]) > 32767 or int(a[3]) < -32768:
                    print('Error, size of immediate')
                    print('Cant assemble line number: ')
                    print(count + 1)
                    print(mips_l)
                    sys.exit()
            reg_s = checkreg(mips_registers, a[2])
            reg_t = checkreg(mips_registers, a[1])
            #print("I entered all other I commands",a,argc)
            stringI = stringI.replace('rt', reg_t)
            stringI = stringI.replace('rs', reg_s)
            stringI = stringI.replace('immediate', immediate)
        stringI = str('%08X' % int(stringI, 2)).lower()
        return stringI
    else:
        print('Error, command does not exist')
        print('Cant assemble line number: ')
        print(count + 1)
        print(mips_l)
        sys.exit()
        #print("The entered command is incorrect",a,argc)
    #convert binary to hex
    return "00000000"

# def convertbranchstatements(mips_before, numline):
#     mips_after =
#     return mips_after



def read_in_write_out_assembly_to_machine(infile, outfile):
    mips_lines = []
    labels = {}
    mips_nolabels = []
    mips_converted = []

    with open (infile, 'r') as filein:
        data=filein.readlines()
        #print(data)
        for i in data:
            val = i.strip().replace(':','').replace(',', '').replace('\t',' ').replace(')', '').replace('(', ' ')
            mips_lines.append(val)

        number = 0
        for m in mips_lines:
            b = mips_lines[number].split(" ")
            argcount = len(b)
            if argcount == 1:
                labels[b[0]] = number
                # del b[number]
                # mips_lines.remove(number)
            #append new mips_line to list without labels
            else:
                mips_nolabels.append(mips_lines[number])

            number = number + 1

        for key in labels:
            locations = [i for i, s in enumerate(mips_nolabels) if key in s]
            for p in locations:
                val = labels[key] - (p + 2)
                if val < 0:
                    val = val + 1
                mips_nolabels[p] = mips_nolabels[p].replace(key, str(val))

        num = 0
        for j in mips_nolabels:
            # temp = mips_lines[1].split(" ")
            # print(mips_commands[temp]
            com = data_convert_mips_line(mips_nolabels[num], num)
            mips_converted.append(com)
            #print(num)
            num = num + 1

    with open (outfile, 'w') as fileout:
        for ele in mips_converted:
            fileout.write('%s\n' % ele)
    #print(mips_converted)


# To test the program all that is required is updating the file paths
# and names to the desired results
def main():
    if len(sys.argv) == 2:
        # argv[1] has your filename
        filenamein = sys.argv[1]
        filenameout = filenamein.replace('.s', '.obj')
        read_in_write_out_assembly_to_machine(filenamein, filenameout)
    else:
        print("Please only input one test file with proper input *.s format")
        sys.exit()
if __name__ == "__main__":
    main()
