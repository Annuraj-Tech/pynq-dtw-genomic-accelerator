#include <iostream>
#include <fstream>
#include <ap_axi_sdata.h>  // Required for hls::axis
#include <hls_stream.h>
#include <ap_int.h>

// AXI-Stream packet typedef matching hls_src.cpp
typedef hls::axis<ap_int<16>, 0, 0, 0> axis_t;

// Function prototype matching top-level accelerator
void dtw_accelerator(hls::stream<axis_t> &in_stream, hls::stream<axis_t> &out_stream);

int main() {
    hls::stream<axis_t> in_stream, out_stream;
    
    // Open signal file extracted from Python script
    std::ifstream file("C:/Users/Annuraj/Downloads/Processed_Signals/signal_0.dat");
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open signal_0.dat file." << std::endl;
        return 1;
    }

    int value;
    int count = 0;
    
    // Read 256 signal samples into the input stream (128 ref + 128 query)
    while (file >> value && count < 256) {
        axis_t pkt;
        pkt.data = (ap_int<16>)value;
        pkt.keep = -1;
        pkt.strb = -1;
        pkt.last = (count == 255) ? 1 : 0;
        in_stream.write(pkt);
        count++;
    }
    file.close();

    std::cout << "Streamed " << count << " signal samples into hardware core..." << std::endl;

    // Run the HLS accelerator function
    dtw_accelerator(in_stream, out_stream);

    // Read hardware output
    if (!out_stream.empty()) {
        axis_t result = out_stream.read();
        std::cout << "Hardware Dynamic Time Warping Cost: " << result.data << std::endl;
    } else {
        std::cout << "Simulation Error: Output stream is empty." << std::endl;
    }

    return 0;
}