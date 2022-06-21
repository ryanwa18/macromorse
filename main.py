import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import
from digitalio import DigitalInOut, Pull
import touchio

print("Morse Code Keyboard")

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

# Function to encrypt the string 
# according to the morse code chart
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
 
            # Looks up the dictionary and adds the
            # corresponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += ' '
 
    return cipher
 
# Function to decrypt the string
# from morse to english
def decrypt(message):
 
    # extra space added at the end to access the
    # last morse code
    message += ' '
 
    decipher = ''
    citext = ''
    for letter in message:
 
        # checks for space
        if (letter != ' '):
 
            # counter to keep track of space
            i = 0
 
            # storing morse code of a single character
            citext += letter
 
        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1
 
            # if i = 2 that indicates a new word
            if i == 2 :
 
                 # adding space to separate words
                decipher += ' '
            else:
 
                # accessing the keys using their values (reverse of encryption)
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''
 
    return decipher

# Hard-coded driver function to run the program
def main():
    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
    pixel.fill(0x0)
    
    time.sleep(1)
    
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

    # create the switch, add a pullup, start it with not being pressed
    button = DigitalInOut(board.SWITCH)
    button.switch_to_input(pull=Pull.DOWN)
    button_state = False
    
    touch = touchio.TouchIn(board.TOUCH)
    touch_state = False
    
    message = ''
    isComplete = False
    count = 0
    space_count = 0
    while not isComplete:
        
        if button.value and not button_state:
            pixel.fill((255, 0, 255))
            button_state = True

        if not button.value and button_state:
            pixel.fill(0x0)
            print("DOT")
            message += '.'
            button_state = False
            time.sleep(1)
            count = 0
            print(message)

        if touch.value and not touch_state:
            pixel.fill((0, 255, 0))
            touch_state = True
        if not touch.value and touch_state:
            print("DASH")
            pixel.fill(0x0)
            message += '-'
            touch_state = False
            time.sleep(1)
            count = 0
            print(message)
        
        if not touch_state and not button_state:
            count += 1
            if count > 10000:
                count = 0
                space_count += 1
                message += ' '
                print ("SPACE")
                print(message)
                time.sleep(1)
            if space_count > 3:
                print ("DECODED MESSAGE:")
                print (decrypt(message.rstrip()))
                isComplete = True
            
        
        
# Executes the main function
if __name__ == '__main__':
    main()


