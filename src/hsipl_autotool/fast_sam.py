import os
import numpy as np
import matplotlib.pyplot as plt
import time

HSI_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../", "hsi_data")
SAM_RESULT_FOLDER = os.path.join(os.path.dirname(__file__), "../../", "sam_results")

def fast_sam(image, target_pixel):
    H, W, C = image.shape
    flat_image = image.reshape(-1, C).astype(np.float32)
    target_pixel = target_pixel.astype(np.float32)

    target_norm = np.linalg.norm(target_pixel)
    pixel_norms = np.linalg.norm(flat_image, axis=1)

    dot_products = np.dot(flat_image, target_pixel)
    denominator = pixel_norms * target_norm

    with np.errstate(divide='ignore', invalid='ignore'):
        cos_theta = np.clip(dot_products / denominator, -1.0, 1.0)
        angles = np.arccos(cos_theta)
        angles[np.isnan(angles)] = 0.0

    sam_map = angles.reshape(H, W)
    return sam_map

def save_sam_plot(sam_map, target_h, target_w, save_path, cmap="viridis"):
    sam_min, sam_max = np.min(sam_map), np.max(sam_map)
    if sam_max - sam_min > 1e-8:
        sam_norm = (sam_map - sam_min) / (sam_max - sam_min)
    else:
        sam_norm = np.zeros_like(sam_map)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(sam_norm, cmap=cmap)
    ax.plot(target_w, target_h, "ro", markersize=8)
    ax.set_title(f"SAM Map with Target @ ({target_h}, {target_w})")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Normalized SAM')

    plt.tight_layout()
    plt.savefig(save_path, dpi=100)
    plt.show()
    plt.close()

def register_tools(mcp):
    @mcp.tool()
    def simple_sam_process(filename: str) -> str:
        """
        Load .npy file, let user click to choose target pixel, 
        then compute, save and plot the SAM map.

        Args:
            filename (str): Filename inside hsi_data folder.

        Returns:
            str: Message indicating completion and saved file path.
        """
        npy_path = os.path.join(HSI_DATA_FOLDER, filename)
        if not os.path.isfile(npy_path):
            return f"檔案不存在: {filename}"

        image = np.load(npy_path)
        if image.ndim != 3:
            return f"錯誤: {filename} 不是一個 3D (H, W, C) 的影像。"

        H, W, C = image.shape

        img_show = image.mean(axis=2)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(img_show, cmap='gray')
        ax.set_title("Click a target pixel for SAM computation")
        
        coords = []

        def onclick(event):
            if event.inaxes is not None:
                target_w = int(round(event.xdata))
                target_h = int(round(event.ydata))
                coords.append((target_h, target_w))
                plt.close()

        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        if not coords:
            return "⚠️ 沒有選取任何座標，請重新執行。"

        target_h, target_w = coords[0]

        if not (0 <= target_h < H and 0 <= target_w < W):
            return f"錯誤: 選取座標 ({target_h}, {target_w}) 超出影像尺寸 ({H}, {W})。"

        # ✅ 選完 target 開始計算 + 儲存 SAM
        start_total = time.time()

        target_pixel = image[target_h, target_w]
        sam_map = fast_sam(image, target_pixel)

        point_folder = os.path.join(SAM_RESULT_FOLDER, "custom_target")
        os.makedirs(point_folder, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(filename))[0]

        # 保存 .npy
        save_npy_path = os.path.join(point_folder, f"{base_name}_h{target_h}_w{target_w}_sam.npy")
        np.save(save_npy_path, sam_map)

        # 保存 .jpg + 畫圖
        save_jpg_path = os.path.join(point_folder, f"{base_name}_h{target_h}_w{target_w}_sam.jpg")
        save_sam_plot(sam_map, target_h, target_w, save_jpg_path)

        end_total = time.time()
        total_time = end_total - start_total

        return f"✅ SAM 運算完成！座標 ({target_h}, {target_w})，檔案儲存於 {save_jpg_path} 和 {save_npy_path} ⏱️ 耗時 {total_time:.4f} 秒"
