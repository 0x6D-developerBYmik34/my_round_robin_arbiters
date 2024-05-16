from decimal import Decimal
from pathlib import Path
import cocotb
from cocotb.triggers import RisingEdge, Timer

from tb_utils import create_clk

from arbiter_models import SimpleArbiterModel


REQ_SEQ_1 = (
    0b10011011,
    0b10011010,
    0b10011000,
    0b10011000,
    0b10001010,
    0b00001010,
)

REQ_SEQ_2 = (
    0b10011010,
    0b10011000,
    0b10011000,
    0b10001010,
    0b00001010,
)


@cocotb.test()
async def tb_arbiter_test_1(dut):
    create_clk(dut.clk)

    dut.rst.value = 1
    dut.req.value = 0
    dut_model = SimpleArbiterModel()
    await Timer(Decimal(10))
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    for req_v in REQ_SEQ_1:
        dut.req.value = req_v
        model_grants = dut_model.do_arbiter(req_v)
        await RisingEdge(dut.clk)
        dut._log.info(
            f"req={bin(dut.req.value)} grants={bin(dut.grants.value)} " 
            f"model_grants={bin(model_grants)}"
        )
        assert dut.grants.value == model_grants

    await RisingEdge(dut.clk)


@cocotb.test()
async def tb_arbiter_test_2(dut):
    create_clk(dut.clk)

    dut.rst.value = 1
    dut.req.value = 0
    dut_model = SimpleArbiterModel()
    await Timer(Decimal(10))
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    for req_v in REQ_SEQ_2:
        dut.req.value = req_v
        model_grants = dut_model.do_arbiter(req_v)
        await RisingEdge(dut.clk)
        dut._log.info(
            f"req={bin(dut.req.value)} grants={bin(dut.grants.value)} " 
            f"model_grants={bin(model_grants)}"
        )
        assert dut.grants.value == model_grants

    await RisingEdge(dut.clk)


@cocotb.test()
async def tb_arbiter_test_3(dut):
    create_clk(dut.clk)

    dut.rst.value = 1
    dut.req.value = 0
    dut_model = SimpleArbiterModel()
    await Timer(Decimal(10))
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    dut.req.value = 0b11111111
    for _ in range(8):
        model_grants = dut_model.do_arbiter(0b11111111)
        await RisingEdge(dut.clk)
        dut._log.info(
            f"req={bin(dut.req.value)} grants={bin(dut.grants.value)} " 
            f"model_grants={bin(model_grants)}"
        )
        assert dut.grants.value == model_grants

    await RisingEdge(dut.clk)
