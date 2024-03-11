import re

# VARIOUS DICTIONARIES

#INSTRUCTION DICTIONARIES:-

Rtype={ #[function7, func3, opcode]
    "add":["0000000","000","0110011"],"sub":["0100000","000","0110011"], "sll":["0000000","001","0110011"],
    "slt":["0000000","010","0110011"],"sltu":["0000000","011","0110011"],"xor":["0000000","100","0110011"],
    "srl":["0000000","101","0110011"],"or":["0000000","110","0110011"],"and":["0000000","111","0110011"]
}


Itype={ #[function3, opcode]
    "lw":["010","0000011"],"addi":["000","0010011"],"sltiu":["011","0010011"],"jalr":["000","1100111"]
}


Stype={ #[function3, opcode]
    "sw":["010","0100011"]
}


Btype={ #[function3, opcode]
    "beq": ["000", "1100011"],"blt": ["100", "1100011"],"bne":["001", "1100011"],
    "bge": ["101", "1100011"],"bltu": ["110", "1100011"], "bgeu": ["111", "1100011"]
}

Utype={ #opcode
    "lui":"0110111","auipc":"0010111"
}

Jtype={ #opcode
    "jal":"1101111",
}


#REGISTER DICTIONARIES
registers= {
    "zero": "00000",    #zero Hard-wired zero 
    "ra": "00001",      #ra   Return Adress
    "sp": "00010",      #sp   Stack pointer
    "gp": "00011",      #gp   Global pointer
    "tp": "00100",      #tp   Thread pointer
    "t0": "00101",      #t0   Temporary reg

    "t1": "00110",      #t1  temporary
    "t2": "00111",      #t2 temporary

    "s0": "01000",      #s0 saved register
    "fp": "01000",      #s0 saved register
    "s1": "01001",      #s1 saved register

    "a0": "01010",     #a0 function arguement
    "a1": "01011",     #a1 function arguement
    "a2": "01100",     #a2 function arguement
    "a3": "01101",     #a3 function arguement
    "a4": "01110",     #a4 function arguement
    "a5": "01111",     #a5 function arguement
    "a6": "10000",     #a6 function arguement
    "a7": "10001",     #a7 function arguement

    "s2": "10010",     #s2 saved register
    "s3": "10011",     #s3 saved register
    "s4": "10100",     #s4 saved register
    "s5": "10101",     #s5 saved register
    "s6": "10110",     #s6 saved register
    "s7": "10111",     #s7 saved register
    "s8": "11000",     #s8 saved register
    "s9": "11001",     #s9 saved register
    "s10": "11010",    #s10 saved register
    "s11": "11011",    #s11 saved register

    "t3": "11100",     #t3 temporary
    "t4": "11101",     #t4 temporary
    "t5": "11110",     #t5 temporary
    "t6": "11111"      #t6 temporary
}

#handling errors
Errors = ["Register error. Register not in ISA","Error. Instruction not in ISA"]

#handling labels
labels = {"start": "00000000000000000000000000000000", "end":"11111111111111111111111111111111"}


def dec_to_binary(given_value): #gives the output as a 32 bit binary string. handles both negative and positive imm values. also handles sext
  if given_value == "end":
      return labels["end"]
  if given_value == "start":
      return labels["start"]
  n = int(given_value)
  m = ""
  i = 32  #32-bit loop
  while i:
    a = n & 1
    m = str(a) + m
    n = n >> 1
    i = i - 1
  return m


def assembly_to_machine(line):
    if line[0] in Rtype:  #handling Rtype instruction
        fn7, fn3, opcode = Rtype[line[0]]
        if(line[1] not in registers or line[2] not in registers or line[3] not in registers):
            return "Register error. Register not in ISA"
        else: 
            return fn7  + registers[line[3]]  + registers[line[2]]  + fn3   + registers[line[1]]  + opcode
        
    
    elif line[0] in Itype: #handling Itype instruction
        fn3, opcode = Itype[line[0]]
        if line[0]=="lw":
            if (line[1] not in registers or line[3] not in registers):
                return "Register error. Register not in ISA"
            else:
                imm = dec_to_binary(line[2])[-12:]
                return imm  + registers[line[3]] + fn3 + registers[line[1]] + opcode
            
        else:
            if (line[1] not in registers or line[2] not in registers):
                return "Register error. Register not in ISA"
            else:
                imm = dec_to_binary(line[3])[-12:]
                return imm + registers[line[2]] + fn3 + registers[line[1]] + opcode
        
        
    
    elif line[0] in Stype: #handling Stype instruction
        fn3, opcode = Stype[line[0]]
        if (line[1] not in registers or line[3] not in registers):
            return "Register error. Register not in ISA"
        else:
            imm = dec_to_binary(line[2])
            return imm[-12:-5] + registers[line[1]] + registers[line[3]] + fn3 + imm[-5:] + opcode 
        
    
    elif line[0] in Btype: #handling Btype instruction
        fn3, opcode = Btype[line[0]]
        if (line[1] not in registers or line[2] not in registers):
            return "Register error. Register not in ISA"
        else:
            imm = dec_to_binary(line[3])
            return imm[-12:-5] + registers[line[2]] + registers[line[1]] + fn3 + imm[-5:] + opcode
        
    
    elif line[0] in Utype:  #handling Utype instruction
        opcode = Utype[line[0]]
        if line[1] not in registers:
            return "Register error. Register not in ISA"
        else:
            imm = dec_to_binary(line[2])
            return imm[-31:-11] + registers[line[1]] + opcode
        
    
    elif line[0] in Jtype:
        opcode = Jtype[line[0]]
        if line[1] not in registers:
            return "Register error. Register not in ISA"
        else:
            imm =dec_to_binary(line[2])
            return imm[-12:-1] + imm[-21:-12] + registers[line[1]] + opcode
    
    else:
        return "Error. Instruction not in ISA"
    
        
    
    
    
    
input = open("input.txt", "r") #opening  the input file
output = open("output.txt", "w") #opening the output file

#reading the lines from input file
l1 = input.readlines()
if l1[-1] != "beq zero,zero,0" and l1[-1] != "end: beq zero,zero,0": #handling the case if the code doesn't end with virtual halt
        output.write("Halt error. No virtual halt statement\n")
else:
    for line in l1:
        line = line.strip() #removed any white space or new line character
        line = [line]
        for word in line:
            word = re.sub("[^A-Z0-9" "-]", " ", word,0,re.IGNORECASE) 
            #using regex to remove all the other special characters from the lines like commas, brackets
            line  = word.split()
            if line[0] == "start" or line[0]=="end":
                line = line[1:]
            data = assembly_to_machine(line) #converting the assembly code to machine code
            output.write(data+"\n")  
            print(line)
        if data in Errors:
            break
    
    
    
input.close()
output.close()
