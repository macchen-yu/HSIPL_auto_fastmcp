# server.py
from mcp.server.fastmcp import FastMCP
import os
import sys

# 加 src 到 Python 模組搜尋路徑
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# 建立 MCP Server 實例（這個 mcp 必須是模組層級變數）
mcp = FastMCP("hsipl_autotool", timeout=300000)

# 註冊 tools
import src.hsipl_autotool.hsi_tools as hsi_tools
import src.hsipl_autotool.hsi_plot as hsi_plot
import src.hsipl_autotool.fast_sam as fast_sam
# import src.sam_stream as sam_stream  # 有的話也可以

hsi_tools.register_tools(mcp)
hsi_plot.register_tools(mcp)
fast_sam.register_tools(mcp)
# sam_stream.register_tools(mcp)

# 確保資料夾存在
HSI_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "hsi_data")
os.makedirs(HSI_DATA_FOLDER, exist_ok=True)

if __name__ == "__main__":  
    """This function will be picked up by uv run, mcpo, or CLI."""
    mcp.run()
