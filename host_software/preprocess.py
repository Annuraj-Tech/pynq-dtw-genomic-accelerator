import numpy as np
import os
import h5py

def preprocess_native_ivt_dataset_final(base_input_dir, output_base_dir, chunk_len=128):
    native_count = 0
    ivt_count = 0
    
    print(f"[INFO] Scanning dataset directory: {base_input_dir}")
    
    if not os.path.exists(base_input_dir):
        print(f"[ERROR] Input directory does not exist: {base_input_dir}")
        return

    for root, dirs, files in os.walk(base_input_dir):
        folder_name = os.path.basename(root).lower()
        
        category = None
        if folder_name == 'native':
            category = 'native'
        elif folder_name == 'ivt':
            category = 'ivt'
            
        if not category:
            continue
            
        target_dir = os.path.join(output_base_dir, category)
        os.makedirs(target_dir, exist_ok=True)
        
        for filename in files:
            if filename.endswith('.fast5'):
                file_path = os.path.join(root, filename)
                
                try:
                    with h5py.File(file_path, 'r') as f5:
                        if 'Raw' in f5 and 'Reads' in f5['Raw']:
                            reads_group = f5['Raw']['Reads']
                            for read_id in reads_group:
                                read_node = reads_group[read_id]
                                if 'Signal' in read_node:
                                    # Extract raw signal directly as int16
                                    raw_signal = np.array(read_node['Signal'], dtype=np.int16)
                                    
                                    if len(raw_signal) < (2 * chunk_len):
                                        continue

                                    # Split into Reference and Query chunks of length 128
                                    ref_chunk = raw_signal[:chunk_len]
                                    query_chunk = raw_signal[chunk_len:2*chunk_len]
                                    
                                    paired_data = np.array([ref_chunk, query_chunk], dtype=np.int16)
                                    
                                    if category == 'native':
                                        out_name = f"native_pair_{native_count:04d}.npy"
                                        np.save(os.path.join(target_dir, out_name), paired_data)
                                        native_count += 1
                                    else:
                                        out_name = f"ivt_pair_{ivt_count:04d}.npy"
                                        np.save(os.path.join(target_dir, out_name), paired_data)
                                        ivt_count += 1
                                    break # Take the first valid read per file
                except Exception:
                    continue

    print(f"\n[SUCCESS] Processing Complete!")
    print(f" -> Processed Native Pairs : {native_count}")
    print(f" -> Processed IVT Pairs    : {ivt_count}")
    print(f" -> Saved to output folder : {output_base_dir}")

if __name__ == "__main__":
    INPUT_DIR = r"C:\Users\Annuraj\Downloads\01_Hsapiens_18S_rRNA_Dataset\01_Hsapiens 18S_rRNA_Dataset"
    OUTPUT_DIR = "./processed_pynq_dataset"
    
    preprocess_native_ivt_dataset_final(INPUT_DIR, OUTPUT_DIR, chunk_len=128)