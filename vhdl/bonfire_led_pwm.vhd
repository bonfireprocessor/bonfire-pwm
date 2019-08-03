----------------------------------------------------------------------------------

-- Create Date:    28.07,2019
-- Design Name:
-- Module Name:
-- The Bonfire Processor Project, (c) 2019 Thomas Hornschuh
-- LED PWM Interface


-- registers:
-- base+0   -- Divider Register
--             Bit 15:0 : Divider for PWM Base Frequency.
--
-- base+4.. base+16:   8 Bit RGB Values for Channels 0..3 :
--  Every register contains an 8 Bit Value for Red, Green, Blue in the lower 24 Bit:
--  Bit 23:16 : Red, Bit 15:8: Green, Bit 7:0: Blue


-- License: See LICENSE or LICENSE.txt File in git project root.
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;


entity bonfire_led_pwm is
  port(
  -- Wishbone ports:
     wb_clk_i   : in std_logic;
     wb_rst_i   : in std_logic;
     wb_adr_i  : in  std_logic_vector(4 downto 2);
     wb_dat_i  : in  std_logic_vector(31 downto 0);
     wb_dat_o : out std_logic_vector(31 downto 0);
     wb_we_i   : in  std_logic;
     wb_cyc_i  : in  std_logic;
     wb_stb_i  : in  std_logic;
     wb_ack_o : out std_logic;

     -- Output Signals
     -- GPIO
     gpio_o : out std_logic_vector(11 downto 0);
     gpio_i : in  std_logic_vector(11 downto 0);
     gpio_t : out std_logic_vector(11 downto 0)

  );

end bonfire_led_pwm;


architecture rtl of bonfire_led_pwm is

  ATTRIBUTE X_INTERFACE_INFO : STRING;
  ATTRIBUTE X_INTERFACE_INFO of  wb_clk_i : SIGNAL is "xilinx.com:signal:clock:1.0 wb_clk_i CLK";
  --X_INTERFACE_INFO of  wb_rst_i : SIGNAL is "xilinx.com:signal:reset:1.0 wb_rst_i RESET";

  ATTRIBUTE X_INTERFACE_PARAMETER : STRING;
  ATTRIBUTE X_INTERFACE_PARAMETER of wb_clk_i : SIGNAL is "ASSOCIATED_BUSIF WB_SLAVE";
  --ATTRIBUTE X_INTERFACE_PARAMETER of rst_i : SIGNAL is "ASSOCIATED_BUSIF WB_DB";

  ATTRIBUTE X_INTERFACE_INFO OF wb_cyc_i: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_cyc_o";
  ATTRIBUTE X_INTERFACE_INFO OF wb_stb_i: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_stb_o";
  ATTRIBUTE X_INTERFACE_INFO OF wb_we_i: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0  WB_SLAVE wb_dbus_we_o";
  ATTRIBUTE X_INTERFACE_INFO OF wb_ack_o: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_ack_i";
  ATTRIBUTE X_INTERFACE_INFO OF wb_adr_i: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_adr_o";
  ATTRIBUTE X_INTERFACE_INFO OF wb_dat_i: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_dat_o";
  ATTRIBUTE X_INTERFACE_INFO OF wb_dat_o: SIGNAL IS "bonfire.eu:wb:Wishbone_master:1.0 WB_SLAVE wb_dbus_dat_i";


  ATTRIBUTE  X_INTERFACE_INFO OF gpio_o: SIGNAL IS "xilinx.com:interface:gpio:1.0 GPIO TRI_O";
  ATTRIBUTE  X_INTERFACE_INFO OF gpio_i: SIGNAL IS "xilinx.com:interface:gpio:1.0 GPIO TRI_I";
  ATTRIBUTE  X_INTERFACE_INFO OF gpio_t: SIGNAL IS "xilinx.com:interface:gpio:1.0 GPIO TRI_T";



  signal red_v           : std_logic_vector(3 downto 0);
  signal green_v         : std_logic_vector(3 downto 0);
  signal blue_v          : std_logic_vector(3 downto 0);

  signal wb_bus_adr      : std_logic_vector(2 downto 0);



  component bonfire_led_pwm_core
  port (
    gpio_o      : out std_logic_vector(11 downto 0);
    clock       : in  std_logic;
    reset       : in  std_logic;
    wb_we       : in  std_logic;
    wb_adr      : in  std_logic_vector(2 downto 0);
    wb_stb      : in  std_logic;
    wb_ack      : out std_logic;
    wb_cyc      : in  std_logic;
    wb_db_read  : out std_logic_vector(31 downto 0);
    wb_db_write : in  std_logic_vector(31 downto 0)
);
end component bonfire_led_pwm_core;



  begin

  wb_bus_adr <= wb_adr_i(wb_adr_i'range);
  gpio_t <= (others=>'0');

  bonfire_led_pwm_core_i : bonfire_led_pwm_core
  port map (

    clock           => wb_clk_i,
    reset           => wb_rst_i,
    wb_we       => wb_we_i,
    wb_adr      => wb_bus_adr,
    wb_stb      => wb_stb_i,
    wb_ack      => wb_ack_o,
    wb_cyc      => wb_cyc_i,
    wb_db_read  => wb_dat_o,
    wb_db_write => wb_dat_i,
    gpio_o          => gpio_o
  );


end rtl;
