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