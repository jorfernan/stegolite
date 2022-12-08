#!/usr/bin/env python
from PIL import Image
import os
from colors import bcolors
import datetime

TITLE = """\n
                __ _                   
  /\/\  _   _  / _\ |_ ___  __ _  ___  
 /    \| | | | \ \| __/ _ \/ _` |/ _ \ 
/ /\/\ \ |_| | _\ \ ||  __/ (_| | (_) |
\/    \/\__, | \__/\__\___|\__, |\___/ 
        |___/              |___/       
\nBy Jorge Fernández Moreno
"""

FLAG = "1111000011001000001111001101"


# Transforms a string of characters into a string of its char binary values
def txt_to_bin_str(txt):
    return ''.join('{0:08b}'.format(ord(x), 'b') for x in txt)

# Transforms an integer into a string of length 8 with its value in binary
def int_to_8_bits_bin(num):
    return ("0"*(8-len(bin(num)[2:]))) + bin(num)[2:]

# Transforms a binary string into an integer
def bin_to_int(bin):
    return int(bin,2)

# Transforms a binary string into an ascii string
def bin_to_ascii(bin):
    return (int(bin,2).to_bytes(int(bin,2).bit_length() + 7 // 8, "big")).decode()

# Gets the image
def getImage(action = "encode"):
    try:
        image = input(bcolors.OKGREEN + "Insert image name "+ bcolors.WARNING +"[ Extension included ]: " + bcolors.ENDC)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        folder = "images" if action == "encode" else "newImages"
        img = Image.open(os.path.join(dir_path,folder,image), 'r')
        return img
    except FileNotFoundError:
        print(f"{bcolors.FAIL + bcolors.BOLD}\nError: {bcolors.ENDC} Image file [{bcolors.WARNING} {image} {bcolors.ENDC}] not found inside images folder.\n{bcolors.FAIL + bcolors.BOLD }Cancelling execution...\n{bcolors.ENDC}")
        exit()

# Gets text to hide
def getText():
    text = input(f"{bcolors.OKGREEN}Insert text to hide: {bcolors.ENDC}")
    if len(text) == 0:
        print(f"{bcolors.FAIL + bcolors.BOLD}\nError! Text not inserted.\nCancelling execution...\n{bcolors.ENDC}")
        exit()
    for char in text:
        if ord(char) < 32 or ord(char) > 126:
            print(f"{bcolors.FAIL + bcolors.BOLD}\nError! Invalid characters inserted.\nCancelling execution...\n{bcolors.ENDC}")
            exit()
    return text.strip()

#Hides data inside the R value
def hide_on_red(image,text):

    data = txt_to_bin_str(text)
    width,height = image.size
    img_data = list(image.getdata())

    if (len(data) + len(FLAG)) > len(img_data):
        print(f"{bcolors.FAIL + bcolors.BOLD}\nError! Data too large.\nCancelling execution...\n{bcolors.ENDC}")
        exit()
    else:
        cont = 0
        for element in data:
            l = list(img_data[cont])
            l[0] = bin_to_int(int_to_8_bits_bin(l[0])[:-1]+ element )
            img_data[cont] = tuple(l)
            cont += 1
        
        for char in FLAG:
            l = list(img_data[cont])
            l[0] = bin_to_int(int_to_8_bits_bin(l[0])[:-1] + char)
            img_data[cont] = tuple(l)
            cont += 1
        
    
    # Currently saving images without alpha
    new_image = Image.new("RGB",(width,height))
    new_image.putdata(img_data)

    return new_image


def saveImage(image, ext = ".jpg"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    now = str(datetime.datetime.now().timestamp()).replace(".","")
    img_name =  now + ext
    image.save(os.path.join(dir_path,"newImages",img_name))

def encode():
    img = getImage()
    txt = getText()
    new_img = hide_on_red(img,txt)
    saveImage(new_img)

def decode():

    img = getImage("decode")
    img_data = list(img.getdata())
    fullData = ""
    flag = ""
    cont = 0

    for pixel in img_data:
        less_significant = int_to_8_bits_bin(pixel[0])[-1]
        fullData+=less_significant
        if len(flag) < len(FLAG):
            flag += less_significant
        else:
            flag = flag[1:] + less_significant

        print("RED -> ",int_to_8_bits_bin(pixel[0]),"| Less -> ",less_significant," | flag -> ",flag, flag == FLAG)
        
        
        


def main():
    try:
        print(f"{bcolors.OKBLUE + bcolors.BOLD}{TITLE}{bcolors.ENDC}")
        print("")
        print(f"{bcolors.OKCYAN + bcolors.BOLD}Features available:{bcolors.ENDC}")
        print("")
        print(f"{bcolors.BOLD}- Encode input text on {bcolors.FAIL}RED{bcolors.ENDC}{bcolors.BOLD} pixel from image {bcolors.WARNING}{'[1]':>7}{bcolors.ENDC}")
        print(f"{bcolors.BOLD}- Decode input text from {bcolors.FAIL}RED{bcolors.ENDC}{bcolors.BOLD} pixel from image {bcolors.WARNING}{'[2]':>5} Development {bcolors.ENDC}")
        print("")
        
        action = input(f"{bcolors.BOLD}{bcolors.WARNING}OPTION: {bcolors.ENDC}")
        
        actions = {
            "1" : encode,
            "2" : decode
        }

    
        if actions.get(action):
            actions.get(action)()
        else:
            print(bcolors.FAIL+bcolors.BOLD+ "Action not found... Cancelling execution... Bye!" + bcolors.ENDC)
    

    except KeyboardInterrupt:
        print(bcolors.FAIL+bcolors.BOLD+ "\n\nExecution cancelled... Bye!" + bcolors.ENDC)

if __name__ == "__main__":
    main()