# PWM Module for RGB LED
# # Each LED "channel" can be configured with an 3* 8 Bit RGB Value

from myhdl import *

from bonfire_pwm_lib import *


@block
def bonfire_led_pwm(wb_bus,red_v,green_v,blue_v,clock,reset,gen_num_channels,sim=True):
    # wb_bus : Wishbone bus Object
    # red_v,green_v,blue_v : vector of red, green, blue PWM output signals
    # clock, reset : as usual
    # gen_num_channels : Number of LED channels

    red_o = [Signal(bool(0)) for i in range(gen_num_channels)]
    green_o = [Signal(bool(0)) for i in range(gen_num_channels)]
    blue_o = [Signal(bool(0)) for i in range(gen_num_channels)]

    # Divider Output
    cnt_en = Signal(bool(True))

    num_registers=gen_num_channels+1 # Channel Registers + Divider Register 
    # Bus Interface signals
    db_read = [Signal(intbv(0)[32:]) for i in range(num_registers)]
    we = [Signal(bool(0)) for i in range(num_registers)]
    adr = Signal(intbv(val=0,min=0,max=num_registers))
    read_ack = Signal(bool(0))
    db_write=Signal(intbv(0)[32:]) # Workarund  to avoid wrong names in VHDL toplevel

    # Module instances 
    # Divider
    divider_inst=divider(we[0],db_write,db_read[0],cnt_en,clock,reset,16)

    # RGB Channels   
    channels =  [ rgb_pwm( we[i] ,db_write,db_read[i],red_o[i-1],green_o[i-1],blue_o[i-1],cnt_en,clock,reset ) for i in range(1,num_registers) ]
   
    if sim:
        @always_seq(clock.posedge,reset=reset)
        def sim_output():

            if wb_bus.stb and wb_bus.cyc and wb_bus.we:
                print "Write to", wb_bus.adr, ":", wb_bus.db_write


    @always_comb
    def bus_comb():

        wr_en=wb_bus.stb and wb_bus.cyc and wb_bus.we
        wb_bus.ack.next=wr_en or read_ack
        adr.next=wb_bus.adr[len(adr):]

        db_write.next=wb_bus.db_write

        for i in range(num_registers):
             # Address decoder
            if wb_bus.adr==i:
                we[i].next = wr_en


    @always_seq(clock.posedge,reset=reset)
    def bus_read():
        wb_bus.db_read.next = db_read[adr]
        if read_ack==True:
            read_ack.next=False
        else:
            read_ack.next = wb_bus.stb and wb_bus.cyc and not wb_bus.we

    @always_comb
    def comb_outputs():
        red_v.next=0
        for i in range(gen_num_channels):
            red_v.next[i]=red_o[i]
            blue_v.next[i]=blue_o[i]
            green_v.next[i]=green_o[i]


    return instances()
