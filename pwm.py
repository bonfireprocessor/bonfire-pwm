from myhdl import block, always_seq,Signal,modbv, always_comb, instances

@block
def pwm(we,bus_in,bus_out,output,cnt_en,clock,reset,gen_bits):

    pwm_counter = Signal(modbv(0)[gen_bits:])
    pwm_next_max = Signal(modbv(0)[gen_bits:])
    pwm_max = Signal(modbv(0)[gen_bits:])
    
    @always_seq(clock.posedge, reset=reset)
    def seq():
         
        if we:
            pwm_next_max.next = bus_in
             
        if cnt_en:
            if pwm_counter== 2**gen_bits-2:
                pwm_counter.next = 0
                pwm_max.next=pwm_next_max
            else:  
                pwm_counter.next = pwm_counter + 1

    
    @always_comb
    def comb():
        output.next= pwm_counter < pwm_max
        bus_out.next=pwm_max  
          

    return instances() 
      