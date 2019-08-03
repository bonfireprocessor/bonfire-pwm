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

    @block
    def simulation_writer(self,start_sig_i,start_address,value_list, finish_sig_o,clock,reset):
        # start_address: int with address to start
        # value_list: List of values to write
        # finish_sig_o: Output signal asserted when finished

        @instance
        def wb_writer():

            yield start_sig_i
            for i in range(len(value_list)):
                yield clock.posedge

                self.cyc.next=True
                self.stb.next=True
                self.adr.next=start_address+i
                self.db_write.next=value_list[i]
                self.we.next=True

                while self.ack==0:
                    yield clock.posedge

                self.cyc.next=False
                self.stb.next=False
                self.we.next=False

            finish_sig_o.next=True

        return instances()


def wb_sim_write(wb, clock, adr, value):

        yield clock.posedge

        wb.cyc.next = True
        wb.stb.next = True
        wb.adr.next = adr
        wb.db_write.next = value
        wb.we.next = True

        yield join(wb.ack.posedge, clock.posedge)

        wb.cyc.next = False
        wb.stb.next = False
        wb.we.next = False


def wb_sim_read(wb, clock, adr):

        yield clock.posedge

        wb.cyc.next = True
        wb.stb.next = True
        wb.adr.next = adr
        wb.we.next = False
        yield clock.posedge

        while wb.ack == 0:
            yield clock.posedge

        wb.cyc.next = False
        wb.stb.next = False
        wb.we.next = False
