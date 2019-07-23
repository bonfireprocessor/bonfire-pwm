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

    red_o = [Signal(bool(0)) for i in range(gen_num_channels)]
    green_o = [Signal(bool(0)) for i in range(gen_num_channels)]
    blue_o = [Signal(bool(0)) for i in range(gen_num_channels)]

    db_read = [Signal(intbv(0))[32:] for i in range(gen_num_channels)]
    we = [Signal(bool(0)) for i in range(gen_num_channels)]
    cnt_en=True 

    test=rgb_bundle() 


    channels =  [ rgb_pwm( we[i] ,wb_bus.db_write,db_read[i],red_o[i],green_o[i],blue_o[i],cnt_en,clock,reset ) for i in range(gen_num_channels) ]  
    # channels=[]
    # for i in range(gen_num_channels):
    #     channels.append(rgb_pwm(we[i] ,wb_bus.db_write,db_read[i],rgb_bundles[i],cnt_en,clock,reset))

    @always_seq(clock.posedge,reset=reset)
    def seq():
     
        if wb_bus.stb and wb_bus.cyc and wb_bus.we:
            print "Write to", wb_bus.adr, ":", wb_bus.db_write

    @always_comb
    def comb():
        wb_bus.ack.next=wb_bus.stb and wb_bus.cyc
        
       
        wr_en=wb_bus.stb and wb_bus.cyc and wb_bus.we
        
       
        for i in range(gen_num_channels):
             # Address decoder 
            if wb_bus.adr==i:
                we[i].next = wr_en
                #wb_bus.db_read.next = db_read[i]
       
    @always_comb
    def comb_outputs():
        red_v.next = ConcatSignal(*reversed(red_o))
        green_v.next = ConcatSignal(*reversed(green_o))
        blue_v.next = ConcatSignal(*reversed(blue_o))    
       
               
    return instances() 
