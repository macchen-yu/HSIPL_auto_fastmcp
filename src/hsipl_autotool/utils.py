import numpy as np
def load_npy_from_file(filepath):
    """從檔案讀取 numpy array"""
    with open(filepath, "rb") as f:
        return np.load(f)