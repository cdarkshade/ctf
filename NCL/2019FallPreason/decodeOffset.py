code = input("Enter code: ")

needOffset = True
offset = 0
i = 0
decoded = ""
for ch in code:
    if needOffset:
        offset = abs(ord("S") - ord(ch))
        print("offset: " + str(offset))
        needOffset = False
    print("ord of char: " + str(ord(ch)))
    if ch != "-" and ord(ch) > 57:
        x = ord(ch) + offset
        if x > ord("Z"):
            x -= 26
        decoded += chr(x)
    else:
        decoded += ch
print(decoded)
