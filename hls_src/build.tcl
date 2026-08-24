# Vivado HLS Automation Script Template
open_project dtw_core_proj
set_top dtw_core
add_files dtw_core.cpp
add_files -tb dtw_testbench.cpp

# Set Zynq-7000 part (PYNQ-Z2)
open_solution "solution1"
set_part {xc7z020clg400-1}
create_clock -period 10 -name default
# csynth_design
# export_design -format ip_catalog
exit