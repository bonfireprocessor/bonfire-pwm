# PWM Module for RGB LED
# # Each LED "channel" can be configured with an 3* 8 Bit RGB Value

from myhdl import *


@block
def bonfire_led_pwm(wb_bus,red_v,green_v,blue_v,clock,reset,gen_num_channels):
    # wb_bus : Wishbone bus Object
    # red_v,green_v,blue_v : vector of red, green, blue PWM output signals
    # clock, reset : as usual
    # gen_num_channels : Number of LED channels 

    @always_seq(clock.posedge,reset=reset)
    def seq():
        print "dummy"
        if wb_bus.stb and wb_bus.cyc and wb_bus.we:
            print "Write to", wb_bus.adr, ":", wb_bus.db_write

    @always_comb
    def comb():
        wb_bus.ack.next=wb_bus.stb and wb_bus.cyc


    return instances()

