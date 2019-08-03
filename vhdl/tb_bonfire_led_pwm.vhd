----------------------------------------------------------------------------------

-- The Bonfire Processor Project, (c) 2019 Thomas Hornschuh
-- LED PWM Interface - Testbench
-- License: See LICENSE or LICENSE.txt File in git project root.
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_led_pwm is

end tb_led_pwm;

architecture tb of tb_led_pwm  is


  signal wb_clk_i : std_logic := '0';
  signal wb_rst_i : std_logic := '0';
  signal wb_adr_i : std_logic_vector(4 downto 2);
  signal wb_dat_i : std_logic_vector(31 downto 0);
  signal wb_dat_o : std_logic_vector(31 downto 0);
  signal wb_we_i  : std_logic;
  signal wb_cyc_i : std_logic;
  signal wb_stb_i : std_logic;
  signal wb_ack_o : std_logic;
  signal gpio_o   : std_logic_vector(11 downto 0);
  signal gpio_i   : std_logic_vector(11 downto 0);
  signal gpio_t   : std_logic_vector(11 downto 0);


    signal TbSimEnded : std_logic := '0';


  -- Clock period definitions
   constant clk_i_period : time := 10 ns;

   signal cont_bus : boolean := false; -- When TRUE Wishbone bus cyles are executed without idle cycle in between


begin

bonfire_led_pwm_i : entity work.bonfire_led_pwm
port map (
  wb_clk_i => wb_clk_i,
  wb_rst_i => wb_rst_i,
  wb_adr_i => wb_adr_i,
  wb_dat_i => wb_dat_i,
  wb_dat_o => wb_dat_o,
  wb_we_i  => wb_we_i,
  wb_cyc_i => wb_cyc_i,
  wb_stb_i => wb_stb_i,
  wb_ack_o => wb_ack_o,
  gpio_o   => gpio_o,
  gpio_i   => gpio_i,
  gpio_t   => gpio_t
);

 wb_clk_i <= not wb_clk_i after clk_i_period/2 when TbSimEnded /= '1' else '0';



Stimulus : process

    variable d,t : std_logic_vector(wb_dat_i'range);
    variable i : natural;

    procedure wb_write(address : in natural; data : in std_logic_vector(wb_dat_i'range)) is
    begin
       wb_adr_i <= std_logic_vector(to_unsigned(address,wb_adr_i'length));
       if not cont_bus then
         wait until rising_edge(wb_clk_i);
       end if;

       wb_dat_i <= data;
       wb_we_i <= '1';
       wb_cyc_i <= '1';
       wb_stb_i <= '1';

       wait  until rising_edge(wb_clk_i) and wb_ack_o = '1' ;
       wb_stb_i <= '0';
       wb_cyc_i <= '0';
       wb_we_i  <= '0';

    end procedure;

    procedure wb_read(address : in natural;
                     data: out std_logic_vector(wb_dat_o'range) )  is
    begin
       wb_adr_i <= std_logic_vector(to_unsigned(address,wb_adr_i'length));
       if not cont_bus then
         wait until rising_edge(wb_clk_i);
       end if;
       wb_we_i <= '1';
       wb_cyc_i <= '1';
       wb_stb_i <= '1';
       wb_we_i <= '0';
       wait until rising_edge(wb_clk_i) and wb_ack_o = '1';
       data:= wb_dat_o;
       wb_stb_i <= '0';
       wb_cyc_i <= '0';
      --wait for clk_period;
    end procedure;

begin
  wait until rising_edge(wb_clk_i); -- synchronize
  wb_rst_i <= '1';
  wait until rising_edge(wb_clk_i); -- synchronize
  wb_rst_i <= '0';

  wb_write(0,X"00000001"); -- divider

  wb_write(1,X"00808080");
  wb_write(2,X"00808080");
  wb_write(3,X"00808080");

  i := 0;
  -- Wait 1024 Clock cycles
  while i<1024 loop
    wait until rising_edge(wb_clk_i);
    i :=  i + 1;
  end loop;

  wb_read(0,d);
  assert d=X"00000001" report "Divider was changed"  severity failure;

  tbSimEnded<='1';
  report "Simulation ended" severity note;


end process;




end architecture;
