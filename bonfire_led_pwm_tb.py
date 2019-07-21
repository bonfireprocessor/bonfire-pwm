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

    def wb_write_sim(wb,adr,value):

        wb.cyc.next=True
        wb.stb.next=True
        wb.adr.next=adr
        wb.db_write.next=value
        wb.we.next=True
        while True:
            yield clock.posedge
            if wb.ack:
                break
        print now(), "Write ack"
        


    @instance
    def stimulus():
        reset.next=True
        yield delay(40)
        reset.next=False 
        yield delay(40)
         
        for i in range(255): 
            wb_bus.cyc.next=True
            wb_bus.stb.next=True
            wb_bus.adr.next=i
            wb_bus.db_write.next=0xff
            wb_bus.we.next=True
            while True:
                yield clock.posedge
                if wb_bus.ack:
                    break
            print now(), "Write ack"

        #while True:
        #    yield wb_write_sim(wb_bus,0,1)
           
      
            #wb_write_sim(wb_bus,0,2)

    return instances()

inst=led_pwm_tb()
inst.convert(hdl='VHDL')
inst.config_sim(trace=True)
inst.run_sim(500)

