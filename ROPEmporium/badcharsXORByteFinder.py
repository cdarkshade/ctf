'''
@Author: Captain Darkshade
Twitter: @cdarkshade
YouTube: Captain Darkshade

Disclaimer: I am not a security professional nor do I consider myself as an expert. 
I am nothing more than a security enthusiast and a beginner at best. Scanning and 
attacking networks and computers without express permission is illegal in many countries. 
Code samples are provided as is and without warranty. All demos conducted in my own isolated lab
'''
badchars = ["b", "i", "c", "/", " ", "f", "n", "s"]

string = "/bin//sh"
encoded = ''
for i in range(30):
    encoded = ''
    valid = True
    for ch in string:
        if str(chr(i ^ ord(ch))) in badchars:
            valid = False
            break
        encoded += str(chr(i ^ ord(ch)))
    if valid:
        print("Encoded: %s XOR Byte: 0x%x" % (encoded,i))
