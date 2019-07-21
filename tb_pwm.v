module tb_pwm;

reg we;
reg [3:0] bus_in;
wire [3:0] bus_out;
wire output;
reg clock;
reg reset;

initial begin
    $from_myhdl(
        we,
        bus_in,
        clock,
        reset
    );
    $to_myhdl(
        bus_out,
        output
    );
end

pwm dut(
    we,
    bus_in,
    bus_out,
    output,
    clock,
    reset
);

endmodule
