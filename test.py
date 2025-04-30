
import os
import numpy as np
from spectral import envi  # Load envi module
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')  # 讓 Matplotlib 使用互動式後端


raw_DATA_FOLDER = "C:/HSIPL_auto_fastmcp/raw_data"


def get_closest_band_image(filename: str, target_wavelength: float = 600.0):
    """Find and return the image at the wavelength closest to the target wavelength."""
    try:
        # Construct full file path
        file_path = os.path.join(raw_DATA_FOLDER, filename)

        # Open the ENVI file using Spectral Python library
        data = envi.open(file_path + ".hdr")

        # Get metadata information (wavelengths is a list of strings, so we convert to float)
        wavelengths = np.array(data.metadata['wavelength'], dtype=float)  # Convert wavelengths to float

        # Convert the image data to numpy array (format: row, sample, band)
        np_data = data.asarray()

        # Find the closest wavelength to the target (scaled index)
        closest_band_idx = np.abs(wavelengths - target_wavelength).argmin() * (
                    np_data.shape[2] / int(wavelengths.shape[0]))

        # If the index is an integer, use it directly
        if closest_band_idx.is_integer():
            closest_band_idx = int(closest_band_idx)
            closest_wavelength = wavelengths[int(closest_band_idx*wavelengths.shape[0]/np_data.shape[2])]
            closest_band_image = np_data[:, :, closest_band_idx]  # Image at the closest wavelength

            # Plot the image for the closest wavelength
            plt.imshow(closest_band_image, cmap='gray')
            plt.title(f"Image at {closest_wavelength} nm")
            plt.colorbar()
            plt.show()

        else:
            # If the index is not an integer, take the two nearest indices
            closest_band_idx_low = int(np.floor(closest_band_idx))
            closest_band_idx_high = int(np.ceil(closest_band_idx))

            # Get the two band images
            low_band_image = np_data[:, :, closest_band_idx_low]
            high_band_image = np_data[:, :, closest_band_idx_high]

            # Plot both images
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))

            axs[0].imshow(low_band_image, cmap='gray')
            axs[0].set_title(f"Image at {wavelengths[int(closest_band_idx_low*wavelengths.shape[0]/np_data.shape[2])]} nm")
            axs[0].axis('off')

            axs[1].imshow(high_band_image, cmap='gray')
            axs[1].set_title(f"Image at {wavelengths[int(closest_band_idx_high*wavelengths.shape[0]/np_data.shape[2])]} nm")
            axs[1].axis('off')

            plt.show()

        # Return the result
        return "已經畫出來"
    except Exception as e:
        return f"Error retrieving the closest band image: {str(e)}"


def test_get_closest_band_image():
    # Test with a known ENVI file and a target wavelength (600 nm)
    filename = 'FX10_RT'  # Replace with a valid file name in the raw_DATA_FOLDER
    target_wavelength = 605.0
    
    # Call the function
    result = get_closest_band_image(filename, target_wavelength)
    
    # Print the results
    if isinstance(result, dict):
        print("Closest Wavelength:", result["closest_wavelength"])
        print("Image Shape:", result["image_shape"])
    else:
        print(result)

# Run the test
test_get_closest_band_image()