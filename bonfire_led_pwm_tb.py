from myhdl import *
from bonfire_led_pwm import bonfire_led_pwm
#from bonfire_led_pwm4 import bonfire_led_pwm4
from wishbone_bundle import *
from ClkDriver import * 


numChannels=4 
values=[0x00205070,0x00ffffff,0x00000000,0x00deadbe]
 
@block
def led_pwm_tb():

    wb_bus = Wishbone_bundle(True,8,0,32,False,False)

    
    red_v=Signal(intbv(0)[numChannels:])
    green_v=Signal(intbv(0)[numChannels:])
    blue_v=Signal(intbv(0)[numChannels:])


    clock  = Signal(bool(0))
    reset = ResetSignal(0, active=1, isasync=False)

    clk_driver= ClkDriver(clock) 

 
    dut=bonfire_led_pwm(wb_bus,red_v,green_v,blue_v,clock,reset,numChannels)

   
    @instance
    def stimulus():
        reset.next=True
        yield delay(40)
        reset.next=False 
        yield delay(40)

   

        for i in range(4): 
            #print i
            yield wb_bus.sim_write(clock,i,values[i])
            #print "resume", i 
        yield delay(256*20)
 
        while True:
            for i in range(4):
                yield wb_bus.sim_read(clock,i)
                print i, wb_bus.db_read
                if values[i]!=wb_bus.db_read:
                    print "Error at address",i  


    return instances()

inst=led_pwm_tb()
#inst.convert(hdl='VHDL')
inst.config_sim(trace=True)
inst.run_sim(50000)

