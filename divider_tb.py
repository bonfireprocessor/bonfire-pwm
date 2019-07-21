from myhdl import *

from ClkDriver import ClkDriver

from divider import divider

@block
def tb_divider():
    length=4

    we=Signal(bool(0))
    bus_in=Signal(modbv(0)[length:])
    bus_out=Signal(modbv(0)[length:])

    output=Signal(bool(0))

    
    clock  = Signal(bool(0))
    reset = ResetSignal(0, active=1, isasync=False)

    clk_driver= ClkDriver(clock) 

    divider_inst = divider(we,bus_in,bus_out,output,clock,reset,length)

    @instance
    def stimulus():
        print("Start")
        reset.next=True
        yield delay(40)
        reset.next=False
        d= 2**length - 2 
        while d >= 0:
            yield output.posedge
            print now(), "ns Output on"
            bus_in.next = d
            we.next = True  
            yield output.negedge
            we.next = False 
            print "Output off"
            d = d - 1  

    return instances()

    
inst=tb_divider()
inst.config_sim(trace=True)
inst.run_sim(5000)


