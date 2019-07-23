# RGB (3*8 Bit) PWM Module

from myhdl import *
from pwm import *

@block
def rgb_pwm(we, bus_in,bus_out,red_o,green_o,blue_o,cnt_en,clock,reset):

    # Bus write slices 
    sl_red=Signal(intbv(0)[8:])
    sl_green=Signal(intbv(0)[8:])
    sl_blue=Signal(intbv(0)[8:])

    # Bus read slices
    red_bus_out=Signal(intbv(0)[8:])
    green_bus_out=Signal(intbv(0)[8:])
    blue_bus_out=Signal(intbv(0)[8:])

    dummy=Signal(intbv(0)[8:])

    red_ch=pwm(we,sl_red,red_bus_out,red_o, cnt_en,clock,reset,8)
    green_ch=pwm(we,sl_green,green_bus_out,green_o,cnt_en,clock,reset,8)
    blue_ch=pwm(we,sl_blue,blue_bus_out,blue_o,cnt_en,clock,reset,8)

    @always_comb
    def comb():
        sl_red.next = bus_in[24:16]
        sl_green.next = bus_in[16:8]
        sl_blue.next = bus_in[8:0]
            
        #bus_out.next=concat(dummy,red_bus_out,green_bus_out,blue_bus_out)

    return instances()