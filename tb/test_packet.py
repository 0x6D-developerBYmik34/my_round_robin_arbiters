from decimal import Decimal
from pathlib import Path
import cocotb
from cocotb.triggers import RisingEdge, Timer

from tb_utils import create_clk

from arbiter_models import PacketArbiterModel


# tuple[req, req_is_last]
REQ_SEQ = (
    (0b10011011, 0b00000000),
    (0b10011011, 0b00000001),
    (0b10011010, 0b00000000),
    (0b10011011, 0b00000010),
    (0b10011001, 0b00000000),
    (0b10011001, 0b00001000),
    (0b10010001, 0b00000000),
    (0b10110001, 0b00010000),
    (0b10100001, 0b00000000),
    (0b10100001, 0b00000000),
    (0b10100001, 0b00000000),
)


@cocotb.test()
async def tb_arbiter_test_1(dut):
    create_clk(dut.clk)

    dut.rst.value = 1
    dut.req.value = 0
    dut.req_is_last.value = 0
    dut_model = PacketArbiterModel()
    await Timer(Decimal(10))
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    for req_v, req_is_last_v in REQ_SEQ:
        dut.req.value = req_v
        dut.req_is_last.value = req_is_last_v
        model_grants = dut_model.do_arbiter(req_v, req_is_last_v)
        await RisingEdge(dut.clk)
        dut._log.info(
            f"req={bin(dut.req.value)} "
            f"req_is_last={bin(dut.req_is_last.value)} "
            f"grants={bin(dut.grants.value)} "
            f"model_grants={bin(model_grants)}"
        )
        assert dut.grants.value == model_grants

    await RisingEdge(dut.clk)


@cocotb.test()
async def tb_arbiter_test_2(dut):
    create_clk(dut.clk)

    dut.rst.value = 1
    dut.req.value = 0
    dut.req_is_last.value = 0
    dut_model = PacketArbiterModel()
    await Timer(Decimal(10))
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    dut.req.value = 0b11111111
    dut.req_is_last.value = 0b11111111
    for _ in range(8):
        model_grants = dut_model.do_arbiter(
            0b11111111,
            0b11111111,
        )
        await RisingEdge(dut.clk)
        dut._log.info(
            f"req={bin(dut.req.value)} "
            f"req_is_last={bin(dut.req_is_last.value)} "
            f"grants={bin(dut.grants.value)} "
            f"model_grants={bin(model_grants)}"
        )
        assert dut.grants.value == model_grants

    await RisingEdge(dut.clk)