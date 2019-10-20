ciphertext = input("Enter ciphertext: ")

needOffset = True
offset = 0
decoded = ""

for ch in ciphertext:
    if needOffset:
        offset = ord("S") - ord(ch)
        needOffset = False
        print("offset: " + str(offset))
    x = ord(ch)
    if x > 64 and x < 91:
        x += offset  
        if x > ord("Z"):
            x -= 26
        elif x < ord("A"):
            x += 26
        decoded += chr(x)
    else:
        decoded += ch
print(decoded)