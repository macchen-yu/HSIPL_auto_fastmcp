import os
import matplotlib.pyplot as plt
from hsipl_autotool.utils import load_npy_from_file

# 指定資料夾路徑
HSI_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../", "hsi_data")
PLOT_RESULT_FOLDER = os.path.join(os.path.dirname(__file__), "../../", "plot_result")

def register_tools(mcp):
    @mcp.tool()
    def list_hsi_files() -> list:
        """List all files in hsi_data folder"""
        return os.listdir(HSI_DATA_FOLDER)

    @mcp.tool()
    def plot_avg_spectrum(filenames: list) -> str:
        """Plot average spectrum for given .npy files, save and show the plot.

        Args:
            filenames (list): List of filenames to load and plot.

        Returns:
            str: Message indicating plot is saved and shown.
        """
        if not filenames:
            return "No files provided."

        # 確保 plot_result 資料夾存在
        os.makedirs(PLOT_RESULT_FOLDER, exist_ok=True)

        plt.figure(figsize=(10, 6))

        for filename in filenames:
            filepath = os.path.join(HSI_DATA_FOLDER, filename)
            if not os.path.isfile(filepath):
                continue
            array = load_npy_from_file(filepath)
            if array.ndim != 3:
                avg_spectrum = array.mean(axis=1)
            else:
                avg_spectrum = array.mean(axis=(0, 1))  # (bands,)
            plt.plot(avg_spectrum, label=filename)

        plt.xlabel("Band")
        plt.ylabel("Average Reflectance")
        plt.title("Average Spectrum of Selected Files")
        plt.legend()
        plt.grid(True)

        # 儲存圖片
        save_path = os.path.join(PLOT_RESULT_FOLDER, "avg_spectrum.png")
        plt.savefig(save_path)

        # 直接打開顯示圖片
        plt.show()

        return f"Average spectrum plot saved to {save_path} and displayed."

