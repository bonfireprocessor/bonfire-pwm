// File: pwm.v
// Generated by MyHDL 0.11
// Date: Sat Jul 20 01:00:30 2019


`timescale 1ns/10ps

module pwm (
    we,
    bus_in,
    bus_out,
    output,
    clock,
    reset
);


input we;
input [3:0] bus_in;
output [3:0] bus_out;
wire [3:0] bus_out;
output output;
wire output;
input clock;
input reset;

reg [3:0] pwm_next_max;
reg [3:0] pwm_max;
reg [3:0] pwm_counter;




assign output = (pwm_counter < pwm_max);
assign bus_out = pwm_max;


always @(posedge clock) begin: PWM_SEQ
    if (reset == 1) begin
        pwm_counter <= 0;
        pwm_max <= 0;
        pwm_next_max <= 0;
    end
    else begin
        if (we) begin
            pwm_next_max <= bus_in;
        end
        if (1'b1) begin
            if (($signed({1'b0, pwm_counter}) == ((2 ** 4) - 2))) begin
                pwm_counter <= 0;
                pwm_max <= pwm_next_max;
            end
            else begin
                pwm_counter <= (pwm_counter + 1);
            end
        end
    end
end

endmodule