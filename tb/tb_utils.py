from cocotb.clock import Clock
import cocotb


CLK_PERIOD = 10


def create_clk(clk_wire):
    clock = Clock(clk_wire, CLK_PERIOD)
    cocotb.start_soon(clock.start(start_high=False))