"""
Bonfire PWM Library
(c) 2019 The Bonfire Project
License: See LICENSE
"""

from myhdl import *


@block
def pwm(we,bus_in,bus_out,output,cnt_en,clock,reset,gen_bits):

    pwm_counter = Signal(modbv(0)[gen_bits:])
    pwm_next_max = Signal(modbv(0)[gen_bits:])
    pwm_max = Signal(modbv(0)[gen_bits:])

    @always_seq(clock.posedge, reset=reset)
    def seq():

        if we:
            pwm_next_max.next = bus_in

        if cnt_en:
            if pwm_counter== 2**gen_bits-2:
                pwm_counter.next = 0
                pwm_max.next=pwm_next_max
            else:
                pwm_counter.next = pwm_counter + 1


    @always_comb
    def comb():
        output.next= pwm_counter < pwm_max
        bus_out.next=pwm_next_max


    return instances()


@block
def divider(we,bus_in,bus_out,en_out,clock,reset,gen_bits):


    counter = Signal(modbv(0)[gen_bits:])
    div = Signal(intbv(0)[gen_bits:])
    zero = Signal(bool(0))


    @always_seq(clock.posedge,reset=reset)
    def seq():

        #print counter.val
        if we:
            div.next = bus_in
            counter.next=0 # Reset counter

        if zero:
            counter.next=div
        else:
            counter.next = counter - 1


    @always_comb
    def comb():
        z = counter == 0
        zero.next = z
        en_out.next  = z

        bus_out.next=div

    return instances()

@block
def rgb_pwm(we, bus_in,bus_out,red_o,green_o,blue_o,cnt_en,clock,reset):


    # Bus out slices
    red_bus_out=Signal(intbv(0)[8:])
    green_bus_out=Signal(intbv(0)[8:])
    blue_bus_out=Signal(intbv(0)[8:])


    red_ch=pwm(we,bus_in(24,16),red_bus_out,red_o, cnt_en,clock,reset,8)
    green_ch=pwm(we,bus_in(16,8),green_bus_out,green_o,cnt_en,clock,reset,8)
    blue_ch=pwm(we,bus_in(8,0),blue_bus_out,blue_o,cnt_en,clock,reset,8)

    @always_comb
    def bus_concat():
        bus_out.next=concat(red_bus_out,green_bus_out,blue_bus_out)


    return instances()
