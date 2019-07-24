# Wishbone Bus interface bundle

from myhdl import *

class Wishbone_bundle:
    def __init__(self,master,adrHigh,adrLow,dataWidth,b4_signals,bte_signals):
        self.cyc = Signal(bool(0))
        self.stb = Signal(bool(0))
        self.ack = Signal(bool(0))
        self.we =  Signal(bool(0))
        self.adr = Signal(intbv(0)[adrHigh:adrLow])
        self.db_write = Signal(intbv(0)[dataWidth:])
        self.db_read =  Signal(intbv(0)[dataWidth:])
        #TODO: Add condionals for b4 and bte signals 
        # if master:
        #     self.cyc.driven=True
        #     self.stb.driven=True
        #     self.we.driven=True 
        #     self.adr.driven=True
        #     self.db_write.driven=True 
        # else:
        #    self.ack.driven=True
        #    self.db_read.driven=True

    
    def sim_write(self,clock, adr, value):

        yield clock.posedge

        self.cyc.next=True
        self.stb.next=True
        self.adr.next=adr
        self.db_write.next=value
        self.we.next=True

        yield join(self.ack.posedge,clock.posedge)

        self.cyc.next=False 
        self.stb.next=False
        self.we.next=False 
        
    def sim_read(self,clock,adr):
    
        yield clock.posedge

        self.cyc.next=True
        self.stb.next=True
        self.adr.next=adr
        self.we.next=False
        yield clock.posedge

        while self.ack==0:
            yield clock.posedge

        self.cyc.next=False 
        self.stb.next=False
        self.we.next=False

        
