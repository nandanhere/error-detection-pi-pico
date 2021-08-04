# Following is the sender code for the raspberry pi pico for the "Reliable data transmission" project by Ben eater,
# for the raspberry pi pico.

from machine import Pin
import utime
from gpio_lcd import GpioLcd
# Pins used for lcd : gpio pins 8 - 13 (in order) for lcd
#                     gpio 0 and 2 were used for clock and data respectively
message = "This is the message to be sent"
TX_RATE = 5 # the number of bits to be sent per second. we keep it small so that the transfer is recognisable
# Two pins will be used to send the data. one for the clock pin, so that on each clock pulse we send a bit, and the other to
# send the bit itself.thus TX_CLK  and TX_DATA
TX_CLK = Pin(2,Pin.OUT)
TX_DATA  = Pin(0,Pin.OUT)
# According to the Gpio_lcd module, the following way we use to declare the lcd with the appropriate pins.
lcd = GpioLcd(rs_pin = Pin(8),enable_pin = Pin(9),
    d4_pin = Pin(10),
    d5_pin = Pin(11),
    d6_pin = Pin(12),
    d7_pin = Pin(13),
    num_lines = 2,
    num_columns = 16)

lcd.clear() # to clear off any characters left in the LCD
lcd.move_to(0,0)
lcd.putstr(message)
lcd.show_cursor()
while True:
    # -----------This section will remove only the top portion of the 2 lined lcd 
    lcd.move_to(0,1)
    lcd.putstr("                ")
    lcd.move_to(0,1)
    # ----------------------------------

    #  Each character in the message is ascii , which are each a byte of data. so we take each character as a byte of information.
    for byte_idx  in range(len(message)):
        char = message[byte_idx]
        num = ord(char) # to get the integer value of the character.
        print(char,end="") # On terminal
        # --------Following section will go through the bit representation of the character and print each bit on the second line
        # =============clearing the bottom line
        lcd.hide_cursor()
        lcd.move_to(0,1)
        lcd.putstr("             ")
        lcd.move_to(byte_idx,0)
        lcd.show_cursor()
        #===================
        # printing each bit on the second line of the lcd one by one
        for bit_idx in range(8):
            tx_bit = num & (0x80 >> bit_idx)
            utime.sleep_ms(int(1000/TX_RATE) // 4)
            TX_CLK.high()  # when this is set to high, the reciever percieves this as a positive edge of the clock
            utime.sleep_ms(int(1000/TX_RATE) // 4)
            if tx_bit:
                TX_DATA.high()
            else:
                TX_DATA.low()
            TX_CLK.low() # when this is set to low, the reciever percieves this as a low edge of the clock.
#           using both the clock and data high and low, the reciever is able to determine a bit value at a given time.
            #update the lcd
            lcd.hide_cursor()
            lcd.move_to(bit_idx,1)
            lcd.putchar("1" if tx_bit else "0")
            lcd.move_to(byte_idx,0)
            lcd.show_cursor()