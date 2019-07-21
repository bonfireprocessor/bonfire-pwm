# Frequency divider for the PWM module

from myhdl import *

@block
def divider(we,bus_in,bus_out,en_out,clock,reset,gen_bits):
    
    counter = Signal(modbv(0)[gen_bits:])
    div = Signal(intbv(2**gen_bits -1)[gen_bits:])

    print div.val, gen_bits

    @always_seq(clock.posedge,reset=reset)
    def seq():

        #print counter.val
        if we:
            div.next = bus_in
            
        if counter == 0:
            counter.next=div
            en_out.next = 1
        else:
            counter.next = counter - 1

        if en_out == 1:
            en_out.next = 0    

    return seq


    