from myhdl import *
from bonfire_led_pwm import bonfire_led_pwm
#from bonfire_led_pwm4 import bonfire_led_pwm4
from wishbone_bundle import *
from ClkDriver import *


numChannels=4
values=(2,0x00205070,0x00ffffff,0x00000000,0x00deadbe)

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

    start=Signal(bool(0))
    finish=Signal(bool(0))
    write_inst=wb_bus.simulation_writer(start,0,values,finish,clock,reset)


    @instance
    def stimulus():
        reset.next=True
        yield delay(40)
        reset.next=False
        yield delay(40)

        #Trigger the simulation writer
        start.next=True
        yield finish

        # for i in range(4):
        #     #print i
        #     yield wb_sim_write(wb_bus,clock,i,values[i])

        yield delay(20)

        for i in range(1):
            for i in range(len(values)):
                yield wb_sim_read(wb_bus,clock,i)
                print i, wb_bus.db_read
                if values[i]!=wb_bus.db_read:
                    print "Error at address",i


    return instances()

inst=led_pwm_tb()

#inst.convert(hdl='VHDL',name='bonfire_led_pwm_tb',path='tb')
#inst.analyze_convert()

inst.config_sim(trace=True)
inst.run_sim(50000)


