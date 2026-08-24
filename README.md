# DTW Hardware Accelerator for m⁶A Detection on PYNQ-Z2

This project provides a full edge-computing hardware-software stack to accelerate the detection of m⁶A RNA modifications directly from raw nanopore electrical signals using a custom Dynamic Time Warping (DTW) systolic array on a Zynq-7000 SoC (PYNQ-Z2).

## Project Structure

* **`hls_src/`**: C++ High Level Synthesis code for the DTW systolic array IP Core.
* **`host_software/`**: Python scripts to run on a powerful host PC for preprocessing signals and running software simulations.
* **`pynq_deployment/`**: Python scripts for board-side execution and streaming data to the FPGA fabric via DMA.
* **`bitstream/`**: Compiled Vivado hardware handoff files (`.bit` and `.hwh`).

---

## Setup & Execution Instructions

### 1. Host PC Preprocessing & Simulation
```bash
cd host_software
python simulate_pc.py

2. Hardware Synthesis (Vivado HLS)
The HLS compiler turns the C++ code into an RTL IP core.

Open Vivado HLS Command Prompt and navigate to the hls_src/ directory.

Use Vivado IP Integrator to connect the generated DTW_Core to a Zynq Processing System via an AXI Direct Memory Access (DMA) block.

Export the bitstream (design_1_wrapper.bit and design_1_wrapper.hwh).

3. PYNQ-Z2 Edge Deployment
Connect your PYNQ-Z2 to your network and open its Jupyter/JupyterLab interface or SSH into it.

Copy the processed dataset, deployment scripts, and bitstream files to the board.

Run the hardware accelerator driver:

python run_pynq_dtw.py --bitstream ../bitstream/design_1_wrapper.bit --data_dir ../dataset/processed_pynq_dataset/native --threshold 50

🌟 Unique Architectural Highlights
Native vs. INT Precision Comparison: Directly evaluates performance, efficiency, and trade-offs between floating-point software reference models and optimized fixed-point integer (int16/int32) hardware execution.

Real-Time DTW Score & Thresholding: Computes dynamic alignment distance metrics on-chip and filters modification patterns instantly using configurable AXI-Lite threshold parameters.

Optimized AXI DMA Memory Management: Implements structured Contiguous Memory Allocation (CMA) buffer handling on the processing system to prevent runtime memory fragmentation during continuous high-throughput batch inference.