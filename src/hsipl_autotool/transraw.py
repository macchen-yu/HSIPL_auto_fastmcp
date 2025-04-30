import os
import numpy as np
from spectral import envi  # Load envi module

# Define the data folder
raw_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../","raw_data")
NPY_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../","hsi_data")

def register_tools(mcp):
    # Tool to load hyperspectral data from a .hdr file
    @mcp.tool()
    def load_hyperspectral_data(filename: str):
        """Load and return hyperspectral data from a given file."""
        try:
            # Construct full file path
            file_path = os.path.join(raw_DATA_FOLDER, filename)
            
            # Open the ENVI file using Spectral Python library
            data = envi.open(file_path+".hdr")
            
            # Get metadata information
            wavelengths = data.metadata['wavelength']
            
            # Convert data to numpy array (format: row, sample, band)
            np_data = data.asarray()
            
            # Log type and shape for debug purposes
            return {
                "data_metadata": str(data),
                "wavelength":str(data.metadata['wavelength']),
                "np_data_shape": np_data.shape
            }
        except Exception as e:
            return f"Error loading hyperspectral data: {str(e)}"

    @mcp.tool()
    def save_hyperspectral_data(filename: str):
        """Save hyperspectral data to a .npy file."""
        try:
            # Construct full file path
            file_path = os.path.join(NPY_DATA_FOLDER, filename)
            
            # Open the ENVI file using Spectral Python library
            data = envi.open(file_path  + ".hdr")
            
            # Convert data to numpy array (format: row, sample, band)
            np_data = data.asarray()
            
            # Save numpy array to .npy file
            np.save(file_path, np_data)
            
            return f"Hyperspectral data saved to {file_path}"
        except Exception as e:
            return f"Error loading hyperspectral data: {str(e)}"

    @mcp.tool()
    def get_closest_band_image_tool(filename: str, target_wavelength: float = 600.0):
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
                closest_wavelength = wavelengths[int(closest_band_idx * wavelengths.shape[0] / np_data.shape[2])]
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
                axs[0].set_title(
                    f"Image at {wavelengths[int(closest_band_idx_low * wavelengths.shape[0] / np_data.shape[2])]} nm")
                axs[0].axis('off')

                axs[1].imshow(high_band_image, cmap='gray')
                axs[1].set_title(
                    f"Image at {wavelengths[int(closest_band_idx_high * wavelengths.shape[0] / np_data.shape[2])]} nm")
                axs[1].axis('off')

                plt.show()

            # Return the result
            return "Image(s) plotted successfully"
        except Exception as e:
            return f"Error retrieving the closest band image: {str(e)}"
            
    @mcp.resource("/raw_data/{filename}")
    def read_raw_data_file(filename: str):
        """Read file content from raw_data"""
        filepath = os.path.join(raw_DATA_FOLDER, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"{filename} not found in raw_data")
        with open(filepath, "rb") as f:
            return f.read()