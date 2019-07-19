from myhdl import block, Signal, ResetSignal, modbv, instances
from myhdl import traceSignals,always,instance,delay,posedge,always_seq

from ClkDriver import ClkDriver

from pwm import pwm 

@block
def tb():
    length=4

    we=Signal(bool(0))
    bus_in=Signal(modbv(0)[length:])
    bus_out=Signal(modbv(0)[length:])

    output=Signal(bool(0))

    clock  = Signal(bool(0))
    reset = ResetSignal(0, active=1, isasync=False)

    clk_driver= ClkDriver(clock) 

    pwm_inst= pwm(we,bus_in,bus_out,output,True,clock,reset,length)

    we_temp=Signal(bool(0))

    @always_seq(clock.posedge, reset=reset)
    def seq():
        we.next = not we and we_temp
             
    @instance
    def stimulus():
        i=0
        k=2**length
        #print k 
        reset.next=True
        yield delay(40)
        reset.next=False
        yield delay(40)
        while i<k:
            #print i 
           
            bus_in.next=i
            we_temp.next=True
           
            yield delay(40)
            we_temp.next=False
            yield delay(20*k*4)
            i=i+1 

    return instances()


inst=tb()
inst.config_sim(trace=True)
inst.run_sim(21000)
inst.convert(hdl='VHDL')
