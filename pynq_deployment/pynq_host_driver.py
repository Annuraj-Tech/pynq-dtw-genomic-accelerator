import numpy as np
import time
import os
from pynq import Overlay, allocate

print("[INFO] Loading bitstream onto FPGA...")
overlay = Overlay("../bitstream/design_1_wrapper.bit")
dma = overlay.axi_dma_0

SEQUENCE_LEN = 128
NUM_BYTES_PER_SAMPLE = 2

in_buffer = allocate(shape=(2 * SEQUENCE_LEN,), dtype=np.int16)
out_buffer = allocate(shape=(1,), dtype=np.int32)

def run_dtw_hardware(ref_seq, query_seq):
    in_buffer[:SEQUENCE_LEN] = ref_seq
    in_buffer[SEQUENCE_LEN:] = query_seq

    dma.sendchannel.transfer(in_buffer)
    dma.recvchannel.transfer(out_buffer)

    dma.sendchannel.wait()
    dma.recvchannel.wait()

    return out_buffer[0]

def process_dataset(dataset_folder):
    file_list = [f for f in os.listdir(dataset_folder) if f.endswith('.npy')]
    results = []
    
    print(f"[INFO] Processing {len(file_list)} signal pairs...")
    
    start_time = time.perf_counter()
    
    for file_name in file_list:
        file_path = os.path.join(dataset_folder, file_name)
        data = np.load(file_path)
        
        ref_seq = data[0].astype(np.int16)
        query_seq = data[1].astype(np.int16)
        
        cost = run_dtw_hardware(ref_seq, query_seq)
        results.append((file_name, cost))
        
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    total_samples = len(file_list) * 2 * SEQUENCE_LEN
    throughput_msps = (total_samples / total_time) / 1e6
    
    print("=" * 45)
    print(f" Total Files Processed : {len(file_list)}")
    print(f" Execution Time        : {total_time:.4f} seconds")
    print(f" Hardware Throughput   : {throughput_msps:.2f} MSPS (Mega-samples/sec)")
    print("=" * 45)
    
    return results

if __name__ == "__main__":
    dataset_path = "../dataset/processed_pynq_dataset/native"
    print(f"[SYSTEM READY] Target dataset: {dataset_path}")