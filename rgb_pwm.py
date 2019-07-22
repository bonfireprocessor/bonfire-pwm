# RGB (3*8 Bit) PWM Module

from myhdl import *
from pwm import *

@block
def rgb_pwm(we, bus_in,bus_out,rgb_bundle,cnt_en,clock,reset):

    # Bus write slices 
    sl_red=bus_in[24:16]
    sl_green=bus_in[16:8]
    sl_blue=bus_in[8:0]

    # Bus read slices
    red_bus_out=Signal(intbv(0)[8:])
    green_bus_out=Signal(intbv(0)[8:])
    blue_bus_out=Signal(intbv(0)[8:])

    dummy=Signal(intbv(0)[8:])

    red_ch=pwm(we,sl_red,red_bus_out,rgb_bundle.red, cnt_en,clock,reset,8)
    green_ch=pwm(we,sl_green,green_bus_out,rgb_bundle.green,cnt_en,clock,reset,8)
    blue_ch=pwm(we,sl_blue,blue_bus_out,rgb_bundle.blue,cnt_en,clock,reset,8)

#     @always_comb
#     def comb():
            
#         bus_out.next=ConcatSignal(dummy,red_bus_out,green_bus_out,blue_bus_out)

    return instances()