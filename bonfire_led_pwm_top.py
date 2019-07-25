from myhdl import *
#from rgb_bundle import *
from bonfire_led_pwm import *
from wishbone_bundle import *

numChannels=4



wb = Wishbone_bundle(False,4,2,32,False,False)

red_v=Signal(intbv(0)[numChannels:])
green_v=Signal(intbv(0)[numChannels:])
blue_v=Signal(intbv(0)[numChannels:])

clock  = Signal(bool(0))
reset = ResetSignal(0, active=1, isasync=False)

bonfire_led_pwm_top = bonfire_led_pwm(wb,red_v,green_v,blue_v,clock,reset,numChannels,sim=False)

bonfire_led_pwm_top.convert(hdl='VHDL',std_logic_ports=True,path='vhdl')

