# PWM Module for RGB LED
# # Each LED "channel" can be configured with an 3* 8 Bit RGB Value

from myhdl import *

from rgb_pwm import *
from rgb_bundle import * 

@block
def bonfire_led_pwm(wb_bus,red_v,green_v,blue_v,clock,reset,gen_num_channels):
    # wb_bus : Wishbone bus Object
    # red_v,green_v,blue_v : vector of red, green, blue PWM output signals
    # clock, reset : as usual
    # gen_num_channels : Number of LED channels 

    rgb_bundles= [rgb_bundle() for i in range(gen_num_channels)]
    db_read = [Signal(intbv(0))[32:] for i in range(gen_num_channels)]
    we = [Signal(bool(0)) for i in range(gen_num_channels)]
    cnt_en=True 




    #channels = rgb_pwm(we[0] ,wb_bus.db_write,db_read[0],rgb_bundles[0],cnt_en,clock,reset)
    #channels =  [rgb_pwm(we[i] ,wb_bus.db_write,db_read[i],rgb_bundles[i],cnt_en,clock,reset) for i in range(gen_num_channels) ]  
    channels=[]
    for i in range(gen_num_channels):
        channels.append(rgb_pwm(we[i] ,wb_bus.db_write,db_read[i],rgb_bundles[i],cnt_en,clock,reset))

    @always_seq(clock.posedge,reset=reset)
    def seq():
     
        if wb_bus.stb and wb_bus.cyc and wb_bus.we:
            print "Write to", wb_bus.adr, ":", wb_bus.db_write

    @always_comb
    def comb():
        wb_bus.ack.next=wb_bus.stb and wb_bus.cyc
        

        wr_en=wb_bus.stb and wb_bus.cyc and wb_bus.we
        for i in range(gen_num_channels):
            we[i].next = wb_bus.adr==i and wr_en

               
    return channels,seq,comb  #instances() 
