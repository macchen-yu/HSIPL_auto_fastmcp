import os
import re

HSI_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../", "hsi_data")

def register_tools(mcp):
    @mcp.tool()
    def list_hsi_files() -> list:
        """List all files in hsi_data folder"""
        return os.listdir(HSI_DATA_FOLDER)

    @mcp.tool()
    def upload_hsi_file(filename: str, content: bytes):
        """Upload or overwrite a file in hsi_data"""
        filepath = os.path.join(HSI_DATA_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        return f"Uploaded {filename}"

    @mcp.tool()
    def delete_hsi_file(filename: str):
        """Delete a file in hsi_data"""
        filepath = os.path.join(HSI_DATA_FOLDER, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"{filename} not found")
        os.remove(filepath)
        return f"Deleted {filename}"

    @mcp.tool()
    def search_hsi_files_regex(pattern: str) -> list:
        """Search files in hsi_data folder using regex pattern (case-insensitive)."""
        files = os.listdir(HSI_DATA_FOLDER)
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            return [f"Invalid regex pattern: {str(e)}"]

        result = [file for file in files if regex.search(file)]
        return result

    @mcp.resource("/hsi_data/{filename}")
    def read_hsi_file(filename: str):
        """Read file content from hsi_data"""
        filepath = os.path.join(HSI_DATA_FOLDER, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"{filename} not found")
        with open(filepath, "rb") as f:
            return f.read()
