from m5stack import *
from m5ui import *
from uiflow import *
import machine
import time

setScreenColor(0x002200)

# Pin assignments
pin_A = machine.Pin(3, machine.Pin.OUT)
pin_B = machine.Pin(1, machine.Pin.OUT)
pin_C = machine.Pin(16, machine.Pin.OUT)
pin_D = machine.Pin(17, machine.Pin.OUT)

digit1 = machine.Pin(18, machine.Pin.OUT)
digit2 = machine.Pin(19, machine.Pin.OUT)
digit3 = machine.Pin(23, machine.Pin.OUT)

# Function to display a digit on the 7-segment display
def display_digit(digit, value):
    if digit == 1:
        digit1.on()
        digit2.off()
        digit3.off()
    elif digit == 2:
        digit1.off()
        digit2.on()
        digit3.off()
    elif digit == 3:
        digit1.off()
        digit2.off()
        digit3.on()
        
    if value == 0:
        pin_A.on()
        pin_B.on()
        pin_C.on()
        pin_D.on()
    elif value == 1:
        pin_A.off()
        pin_B.on()
        pin_C.on()
        pin_D.on()
    elif value == 2:
        pin_A.on()
        pin_B.off()
        pin_C.on()
        pin_D.on()
    elif value == 3:
        pin_A.off()
        pin_B.off()
        pin_C.on()
        pin_D.on()
    elif value == 4:
        pin_A.on()
        pin_B.on()
        pin_C.off()
        pin_D.on()
    elif value == 5:
        pin_A.off()
        pin_B.on()
        pin_C.off()
        pin_D.on()
    elif value == 6:
        pin_A.on()
        pin_B.off()
        pin_C.off()
        pin_D.on()
    elif value == 7:
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.on()
    elif value == 8:
        pin_A.on()
        pin_B.on()
        pin_C.on()
        pin_D.off()
    elif value == 9:
        pin_A.off()
        pin_B.on()
        pin_C.on()
        pin_D.off()
    else:
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
     
    time.sleep_ms(10)
    digit1.off()
    digit2.off()
    digit3.off()

# Function to show a count on the 7-segment display
def show_count(num):
    if num < 0 or num > 999:
        # Turn off all segments if the number is out of range
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.on()
        digit3.on()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        return
    
    digits = [0, 0, 0]
    digits[0] = num % 10
    digits[1] = (num // 10) % 10
    digits[2] = (num // 100) % 10
    
    if digits[2] == 0 and digits[1] == 0:
        # Display only the units digit
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.on()
        digit3.off()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)
    elif digits[2] == 0:
        # Display tens and units digits
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        display_digit(2, digits[1])
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)
    else:
        # Display hundreds, tens, and units digits
        time.sleep_ms(10)
        display_digit(1, digits[2])
        time.sleep_ms(10)
        display_digit(2, digits[1])
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)

# Main loop to test the show_count function
for i in range(110):
  show_count(-1)





