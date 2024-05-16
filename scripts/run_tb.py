import sys
import subprocess


SIMPLE_ARBITR_PATH = "../hdl/simple_arbiter.sv ../tb/tb_arbiter.sv"
RR_PACKET_ARBITR_PATH = "../hdl/packet_arbiter.sv ../tb/tb_packet_arbiter.sv"

chooise_dict = {
        "-a": SIMPLE_ARBITR_PATH, 
        "-p": RR_PACKET_ARBITR_PATH, 
}

if __name__ == '__main__':
    path = ""
    try:
        path = chooise_dict[sys.argv[-1]]
    except KeyError:
        path = chooise_dict["-a"]

    res = subprocess.run(
        "iverilog -o out/a.out -g2005-sv " + path
    )
    res.check_returncode()

    print("Compile done!")
    print("Start testbench")
    subprocess.run("vvp out/a.out")

    print()
    a = input("Open wave? (y/n): ")

    if a == 'y':
        subprocess.run('vsim -l "out/transcript" -do open_wave.tcl')
