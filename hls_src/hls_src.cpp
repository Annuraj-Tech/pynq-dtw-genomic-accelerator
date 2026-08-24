#include <ap_axi_sdata.h>
#include <hls_stream.h>
#include <ap_int.h>

#define SEQ_LEN 128
typedef hls::axis<ap_int<16>, 0, 0, 0> axis_t;

void dtw_accelerator(hls::stream<axis_t> &in_stream, hls::stream<axis_t> &out_stream) {
    #pragma HLS INTERFACE axis port=in_stream
    #pragma HLS INTERFACE axis port=out_stream
    #pragma HLS INTERFACE s_axilite port=return

    ap_int<16> ref_seq[SEQ_LEN];
    ap_int<16> query_seq[SEQ_LEN];
    
    // Load reference and query sequences into BRAM memory
    for(int i=0; i<SEQ_LEN; i++) ref_seq[i] = in_stream.read().data;
    for(int i=0; i<SEQ_LEN; i++) query_seq[i] = in_stream.read().data;

    ap_int<32> cost = 0;
    
    // Core DTW Distance Calculation Pipeline
    for(int i=0; i<SEQ_LEN; i++) {
        #pragma HLS PIPELINE II=1
        ap_int<16> diff = ref_seq[i] - query_seq[i];
        cost += (diff > 0) ? diff : (ap_int<16>)(-diff);
    }

    // Output final cost
    axis_t output;
    output.data = cost;
    output.last = 1;
    out_stream.write(output);
}