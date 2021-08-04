# Following is the reciever code for the raspberry pi pico for the "Reliable data transmission" project by Ben eater,
# for the raspberry pi pico.
from machine import Pin
import utime
from gpio_lcd import GpioLcd
# Pins used for lcd : gpio pins 8 - 13 (in order) for lcd
#                     gpio 18 and 19 were used for data and clock respectively

#  the message will be caught in the message variable
message = "" 
TX_RATE = 5
# RX_DATA will recieve the bits in the message. We can connect an led to this pin to indicate recieving
#  instead of the lcd if lcd is unavailable 
RX_DATA = Pin(18,Pin.IN)
# RX_CLK_PULSE will recieve the "clock pulses" of the sender, so that it can be in sync with each bit recieved.
RX_CLK_PULSE = Pin(19,Pin.IN,Pin.PULL_UP)
# this synch however does not ensure that the data will be proper. in my case i found that my reciever was 3 bits out of sync
# most of the times. so i added the counter variable to count to 3 and then start recieving the bytes. This ensured i got the 
# message at the reciever end

counter = 0
bit_position = 0
rx_byte = 0
update_lcd = True
counter = 0
# What the reciever should do when it recieves a clock pulse along with a bit
def get_bit(pin):
    global counter,bit_position,rx_byte,message,update_lcd
    counter += 1
    if counter < 3 : return 
    rx_bit = RX_DATA.value()
    bit_position += 1
    if bit_position >= 8:
        bit_position = 0
        message += chr(rx_byte)
        print(chr(rx_byte)) # for terminal
        rx_byte = 0
    print(rx_bit,end = "")
    if rx_bit:
        rx_byte |= (0x80 >> bit_position)
    update_lcd = True

# we set the pin that collects the clock pulse to act in such a way that, when it has a high value, it will follow something
# called an interrupt request. here, the function named get_bit will be called to catch the bit
RX_CLK_PULSE.irq(trigger = Pin.IRQ_RISING, handler = get_bit)

# a small time delay to allow the sender to start sending
utime.sleep_ms(100)

# We initialise the lcd like in the sender side
lcd = GpioLcd(rs_pin = Pin(8),enable_pin = Pin(9),
    d4_pin = Pin(10),
    d5_pin = Pin(11),
    d6_pin = Pin(12),
    d7_pin = Pin(13),
    num_lines = 2,
    num_columns = 16)

while True:
    if update_lcd:
        # do not update the lcd till a bit has been captured.
        update_lcd = False
        lcd.move_to(0,0)
        lcd.putstr(message)
        if len(message) > 16:
            message = ""
            lcd.move_to(0,0)
            lcd.putstr("                ")
        lcd.move_to(0,1)    
        for i in range(8):
            lcd.putchar("1" if (rx_byte & (0x80 >> i)) else "0")

        

