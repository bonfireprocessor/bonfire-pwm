from myhdl import *
from bonfire_led_pwm import *
from wishbone_bundle import *
from ClkDriver import * 


    


@block
def led_pwm_tb():

    wb_bus = Wishbone_bundle(True,8,0,32,False,False)

    numChannels=1 

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
         
        for i in range(256): 
       
            #print i
            yield wb_bus.sim_write(clock,i,0xdeadbeef)
            #print "resume", i 
           

    return instances()

inst=led_pwm_tb()
#inst.convert(hdl='VHDL')
inst.config_sim(trace=True)
inst.run_sim(500)

