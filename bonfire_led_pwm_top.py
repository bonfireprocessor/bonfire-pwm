from myhdl import *
from bonfire_led_pwm import *
from wishbone_bundle import *

numChannels=4



wb = Wishbone_bundle(False,5,2,32,False,False)

clock  = Signal(bool(0))
reset = ResetSignal(0, active=1, isasync=False)

gpio_o = Signal(intbv(0)[numChannels*3:])


@block
def bonfire_led_pwm_top(wb,gpio_o,clock,reset):

    red_v=Signal(intbv(0)[numChannels:])
    green_v=Signal(intbv(0)[numChannels:])
    blue_v=Signal(intbv(0)[numChannels:])

    inst_0 = bonfire_led_pwm(wb,red_v,green_v,blue_v,clock,reset,numChannels,sim=False)


    @always_comb
    def comb():
        for i in range(numChannels):
            gpio_o[i*3+2].next = red_v[i]
            gpio_o[i*3+1].next = green_v[i]
            gpio_o[i*3].next   = blue_v[i]

    return instances()

top_inst=bonfire_led_pwm_top(wb,gpio_o,clock,reset)


top_inst.convert(hdl='VHDL',std_logic_ports=True,path='vhdl_gen',name='bonfire_led_pwm_core')

