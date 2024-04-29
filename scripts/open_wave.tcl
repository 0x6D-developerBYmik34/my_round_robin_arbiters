# transcript file "out/transcript"
vcd2wlf "out/tb.vcd" "out/tb.wlf"
vsim -view "out/tb.wlf"
# add wave -r *
