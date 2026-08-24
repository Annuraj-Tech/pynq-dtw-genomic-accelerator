import numpy as np
import os
from fastdtw import fastdtw

def run_software_simulation(dataset_dir, max_samples=50):
    """
    Loads processed .npy pairs, runs software DTW using a simple absolute difference, 
    and returns the average distance score.
    """
    if not os.path.exists(dataset_dir):
        print(f"[WARNING] Directory not found: {dataset_dir}")
        return []
        
    file_list = [f for f in os.listdir(dataset_dir) if f.endswith('.npy')][:max_samples]
    distances = []
    
    print(f"[INFO] Running software DTW on {len(file_list)} files from {os.path.basename(dataset_dir)}...")
    
    for filename in file_list:
        file_path = os.path.join(dataset_dir, filename)
        paired_data = np.load(file_path)
        
        # Ensure they are flat 1D arrays of floats
        ref_seq = paired_data[0].astype(np.float32).flatten()
        query_seq = paired_data[1].astype(np.float32).flatten()
        
        # Use a simple absolute difference for scalar comparison
        dtw_distance, _ = fastdtw(ref_seq, query_seq, dist=lambda a, b: abs(a - b))
        distances.append(dtw_distance)
        
    return distances

if __name__ == "__main__":
    native_folder = "./processed_pynq_dataset/native"
    ivt_folder = "./processed_pynq_dataset/ivt"
    
    native_scores = run_software_simulation(native_folder, max_samples=50)
    ivt_scores = run_software_simulation(ivt_folder, max_samples=50)
    
    if native_scores and ivt_scores:
        avg_native = np.mean(native_scores)
        avg_ivt = np.mean(ivt_scores)
        
        print("\n" + "="*40)
        print(" SOFTWARE SIMULATION RESULTS SUMMARY")
        print("="*40)
        print(f" Average Native DTW Score : {avg_native:.2f}")
        print(f" Average IVT Control Score  : {avg_ivt:.2f}")
        print("="*40)
        print("[ANALYSIS] Notice the difference between modified (native)")
        print("           and unmodified (ivt) RNA signal warping distances!")
    else:
        print("[ERROR] No data found to simulate. Check your dataset paths.")