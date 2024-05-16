from cocotb.runner import get_runner
from pathlib import Path
import sys


if __name__ == '__main__':
    sim = "icarus"
    # sim = "questa"

    proj_path = Path(__file__).resolve().parent.parent
    print(proj_path)

    

    hdl_toplevel = "simple_arbiter"
    test_module = "test_simple"

    print(sys.argv)

    if sys.argv[-1] == "-p":
        hdl_toplevel = "packet_arbiter"
        test_module = "test_packet"

    try:
        sim = sys.argv[-2]

    except IndexError:
        print("icarus default")
        
    runner = get_runner(sim)
    runner.build(
        verilog_sources=[
            proj_path / "hdl" / "packet_arbiter.sv",
            proj_path / "hdl" / "simple_arbiter.sv",
        ],
        hdl_toplevel=hdl_toplevel,
        always=True,
    )

    runner.test(
        hdl_toplevel=hdl_toplevel, 
        test_module=test_module,
        waves=True,
    )