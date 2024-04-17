
import sys

# dictionaries for different opcodes

r_type_opcode = ["0110011"]
i_type_opcode = ["0000011", "0010011", "1100111"]
s_type_opcode = ["0100011"]
b_type_opcode = ["1100011"]
u_type_opcode = ["0110111", "0010111"]
j_type_opcode = ["1101111"]

program_counter = 0

data_mem = {'0x00010000': '00000000000000000000000000000000', '0x00010004': '00000000000000000000000000000000', '0x00010008': '00000000000000000000000000000000',
            '0x0001000c': '00000000000000000000000000000000', '0x00010010': '00000000000000000000000000000000', '0x00010014': '00000000000000000000000000000000', 
            '0x00010018': '00000000000000000000000000000000', '0x0001001c': '00000000000000000000000000000000', '0x00010020': '00000000000000000000000000000000', 
            '0x00010024': '00000000000000000000000000000000', '0x00010028': '00000000000000000000000000000000', '0x0001002c': '00000000000000000000000000000000', 
            '0x00010030': '00000000000000000000000000000000', '0x00010034': '00000000000000000000000000000000', '0x00010038': '00000000000000000000000000000000', 
            '0x0001003c': '00000000000000000000000000000000', '0x00010040': '00000000000000000000000000000000', '0x00010044': '00000000000000000000000000000000', 
            '0x00010048': '00000000000000000000000000000000', '0x0001004c': '00000000000000000000000000000000', '0x00010050': '00000000000000000000000000000000', 
            '0x00010054': '00000000000000000000000000000000', '0x00010058': '00000000000000000000000000000000', '0x0001005c': '00000000000000000000000000000000', 
            '0x00010060': '00000000000000000000000000000000', '0x00010064': '00000000000000000000000000000000', '0x00010068': '00000000000000000000000000000000', 
            '0x0001006c': '00000000000000000000000000000000', '0x00010070': '00000000000000000000000000000000', '0x00010074': '00000000000000000000000000000000', 
            '0x00010078': '00000000000000000000000000000000', '0x0001007c': '00000000000000000000000000000000'}

# Binary strings
registers = {
  '00000': "00000000000000000000000000000000",
  '00001': "00000000000000000000000000000000",
  '00010': "00000000000000000000000100000000",
  '00011': "00000000000000000000000000000000",
  '00100': "00000000000000000000000000000000",
  '00101': "00000000000000000000000000000000",
  '00110': "00000000000000000000000000000000",
  '00111': "00000000000000000000000000000000",
  '01000': "00000000000000000000000000000000",
  '01001': "00000000000000000000000000000000",
  '01010': "00000000000000000000000000000000",
  '01011': "00000000000000000000000000000000",
  '01100': "00000000000000000000000000000000",
  '01101': "00000000000000000000000000000000",
  '01110': "00000000000000000000000000000000",
  '01111': "00000000000000000000000000000000",
  '10000': "00000000000000000000000000000000",
  '10001': "00000000000000000000000000000000",
  '10010': "00000000000000000000000000000000",
  '10011': "00000000000000000000000000000000",
  '10100': "00000000000000000000000000000000",
  '10101': "00000000000000000000000000000000",
  '10110': "00000000000000000000000000000000",
  '10111': "00000000000000000000000000000000",
  '11000': "00000000000000000000000000000000",
  '11001': "00000000000000000000000000000000",
  '11010': "00000000000000000000000000000000",
  '11011': "00000000000000000000000000000000",
  '11100': "00000000000000000000000000000000",
  '11101': "00000000000000000000000000000000",
  '11110': "00000000000000000000000000000000",
  '11111': "00000000000000000000000000000000"
}




# dec to heaxdec code
# gives the output as a 32 bit binary string. handles both negative and positive imm values. also handles sext

def dec_to_binary(given_value):  #given value is a string
    n = int(given_value)
    m = ""
    i = 32  # 32-bit loop
    while i:
        a = n & 1
        m = str(a) + m
        n = n >> 1
        i = i - 1
    return m

def binary_to_dec(binary_str):  #handles both the signed and unsigned cases
    if binary_str[0] == '1':
        return -1 * (int(''.join('1' if b == '0' else '0' for b in binary_str), 2) + 1)
    else:
        return int(binary_str, 2)


def rtype(line):
    global program_counter
    rd= line[-12:-7]
    func3 = line[-15:-12]
    rs1 = line[-20:-15]
    rs2 = line[-25:-20]
    func7 = line[-32:-25] 
    
    if (func3 == "000"):
        if(func7 == "0000000"): #add operation
            registers[rd] = dec_to_binary(str(binary_to_dec(registers[rs1]) + binary_to_dec(registers[rs2])))
            
        elif(func7 == "0100000"): #sub operation
            registers[rd] = dec_to_binary(str(binary_to_dec(registers[rs1]) - binary_to_dec(registers[rs2])))
            
    elif(func3 == "001"): #sll operation
        shift = int(registers[rs2][-5:],2)
        registers[rd]=(registers[rs1]+"0"*shift)[-32:]
        
    elif(func3 == "010"): #slt operation
        if(binary_to_dec(registers[rs1]) < binary_to_dec(registers[rs2])):
            registers[rd] = dec_to_binary("1")
            
            
    elif(func3 == "011"): #sltu operation
        if(int(registers[rs1], 2) < int(registers[rs2],2)):
            registers[rd] = dec_to_binary("1")
            
    elif(func3 == "100"): #xor operation
        registers[rd] = registers[rs1] ^ registers[rs2]
        
    elif(func3 == "101"): #srl operation
        shift = int(registers[rs2][-5:],2)
        registers[rd]=("0"*shift+registers[rs1])[:32]
        
    elif(func3 == "110"): #or operation
        registers[rd] = registers[rs1] or registers[rs2]
        
    elif(func3 == "111"): #and operation
         registers[rd] = registers[rs1] and registers[rs2]
         
  
         
def itype(line):
    global program_counter
    line = line[::-1]
    opcode = line[0:7][::-1]
    rd = line[7:12][::-1]
    func3 = line[12:15][::-1]
    rs1 = line[15:20][::-1]
    imm = line[20:32][::-1]
    
    if(func3 == "010"): #lw operation
        rs1_val = binary_to_dec(registers[rs1]) 
        imm_val = binary_to_dec(imm)
        
        print(rs1_val)
        print(imm_val)
        temp = rs1_val + imm_val #integer value
        print(temp)
        registers[rd] = data_mem["0x000" + str(hex(temp))[2:]]
    
    elif(func3 == "000" and opcode == "0010011"):  #addi operation
        rs1_val = binary_to_dec(registers[rs1]) 
        imm_val = binary_to_dec(imm)
        temp = rs1_val + imm_val #integer value
        
        registers[rd] = dec_to_binary(str(temp))
        
    elif(func3 == "011"):    #sltiu operation
        if(int(rs1,2)<int(imm,2)):
            registers[rd] = dec_to_binary("1")
            
    elif(func3 == "000" and opcode == "1100111"):
        val = program_counter
        val +=4
        registers[rd] = dec_to_binary(str(val))
        
        program_counter = binary_to_dec(registers[rs1]) + binary_to_dec(imm)
        
 
    
def btype(line):
    global program_counter
    imm = line[0]+line[-8]+line[1:7]+line[-12:-8]+'0'
    func3 = line[-15:-12]

    rs1 = line[-20:-15]
    rs2 = line[-25:-20]

    

    rs1_sig_val = binary_to_dec(registers[rs1])
    rs2_sig_val = binary_to_dec(registers[rs2])
    rs1_unsig_val = int(registers[rs1], 2)
    rs2_unsig_val = int(registers[rs2], 2)

    imm_val = binary_to_dec(imm)

    if (func3 == "000"):
        if (rs1_sig_val == rs2_sig_val):
            program_counter += imm_val
    elif (func3 == "001"):
        if (rs1_sig_val != rs2_sig_val):
            program_counter += imm_val
    elif (func3 == "100"):
        if (rs1_sig_val < rs2_sig_val):
            program_counter += imm_val
    elif (func3 == "101"):
        if (rs1_sig_val >= rs2_sig_val):
            program_counter += imm_val
    elif (func3 == "110"):
        if (rs1_unsig_val < rs2_unsig_val):
            program_counter += imm_val
    elif (func3 == "111"):
        if (rs1_unsig_val >= rs2_unsig_val):
            program_counter += imm_val
            

            
def stype(line):
    
    global program_counter
    rs2 = line[-25:-20]
    rs1 = line[-20:-15]
    
    imm = line[-32:-25] + line[-12:-7]
    
    imm_dec = binary_to_dec(imm)
    rs1_dec = binary_to_dec(registers[rs1])
    
    add = imm_dec+rs1_dec
    
    data_mem["0x000"+hex(add)[2:]] = registers[rs2]



def utype(line):
    
    global program_counter
    opcode = line[-7::]
    rd = line[-12:-7]
    imm = line[-32:-12]
    
    imm = imm + 12*'0'
    
    if opcode=="0110111":
        #lui
        registers[rd]=imm
    else:
        #auipe
        registers[rd]= dec_to_binary(str(program_counter + binary_to_dec(imm)))



def jtype(line): 
    
    global program_counter
    
    imm = line[-32] + line[-20:-12] + line[-21] + line[-31:-21] + "0"
    rd = line[-12:-7]
    registers[rd] = dec_to_binary(str(program_counter+4))
    
    temp = binary_to_dec(imm)
    
    program_counter = program_counter + temp





#driver code

input = sys.argv[-2]
output = sys.argv[-1]

input_file = open(input)

input_lines = input_file.readlines()

while True:
    l = input_lines[program_counter//4] #line number
    l = l.strip()
    
    
    if (l==""):
        continue
    
    
    #virtual halt
    elif (l == "00000000000000000000000001100011"):
        output.write("0b" + dec_to_binary(program_counter)+ " ")
        for i in registers:
            output.write("0b"+registers[i]+ " ")
        output.write("\n")
        break
    
    else:
        opcode = l[-7:]
        
        if opcode in r_type_opcode:
            rtype(l)
            program_counter+=4
            
        elif opcode in i_type_opcode:
            temp = program_counter
            itype(l)
            if(temp == program_counter):
                program_counter+=4
            
        elif opcode in b_type_opcode:
            temp = program_counter
            btype(l)
            if(program_counter==temp):
                program_counter+=4
        
        elif opcode in s_type_opcode:
            stype(l)
            program_counter+=4
        
        elif opcode in utype(l):
            utype(l)
            program_counter+=4
            
        elif opcode in j_type_opcode:
            jtype(l)
            
        
        output.write("0b" + dec_to_binary(program_counter)+ " ")
        
        for i in registers:
            output.write("0b"+registers[i]+ " ")
        output.write("\n")

for i in data_mem:
    output.write(i+":"+"0b"+data_mem[i] + "\n")
        

