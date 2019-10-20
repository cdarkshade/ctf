charslist = [" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

encoded = input("Enter encoded string: ")
encoded = encoded.strip('"')
encoded = encoded.strip("?")

words = encoded.split(" ")

for word in words:
    chars = word.split("-")
    for ch in chars:
        index = int(ch)
        if index > 0 and index < 28:
            print(charslist[index], end="")
        else:
            print(ch, end="")
    print(" ", end="")
