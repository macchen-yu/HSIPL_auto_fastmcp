# HSIPL Autotool - 安裝指南

本教學將指引你在 **Windows PowerShell** 上安裝必要環境，包括：

- Node.js
- Python 12
- uv 套件管理器

---

## 1. 安裝 uv

在 PowerShell 中執行以下指令以安裝 uv：

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

如果安裝 uv 後出現 `找不到 uv` 的錯誤，可以執行以下命令臨時新增路徑環境變數：

```shell
echo $HOME\.local\bin;$env
```
將文字手動新增到環境變量
---

## 2. 安裝 Node.js

前往 [Node.js 官方網站](https://nodejs.org/en) 下載安裝檔，安裝時請勾選「Add to PATH」選項：

![Node.js 安裝畫面](./pic/nodejs_install.png)

---



## 3. 下載專案

使用 Git 將專案下載至本地端：

```shell
git clone <專案網址>
```

下載完成後，切換至專案資料夾：

```shell
cd HSIPL_fastmcp
```

---

## 4. 安裝server.py

uv run fastmcp install server.py  # 這個要在全局環境裡面先安裝!!!!!!

---
設定檔json
```json
{
  "mcpServers": {
    "hsipl_autotool": {
      "command": "uv",
      "args": [
        "run",
        "fastmcp",
        "run",
        "c:/Users/User/Desktop/HSIPL_fastmcp/server.py"  # 這裡要改成你的專案路徑
      ]
    }
  }
}


```





## 5. 除錯開發 MCP Server

啟動 server 端服務器：

```shell
uv run fastmcp dev server.py
```

啟動成功後，會看到類似下方訊息：

```
Stdio transport: command=C:\Users\User\.local\bin\uv.exe, args=run,--with,mcp,mcp,run,server.py
Spawned stdio transport
Connected MCP client to backing server transport
Created web app transport
Created web app transport
Set up MCP proxy
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

可透過瀏覽器開啟 [http://127.0.0.1:6274](http://127.0.0.1:6274) 查看 MCP Inspector。

---



## 參考資料

- [oalieno - MCP 架設教學](https://oalieno.tw/posts/mcp)
- [MCP 官方教學（miniasp 部落格）](https://blog.miniasp.com/post/2025/04/01/Write-your-own-MCP-server-using-uv-and-Python?full=1&fbclid=IwZXh0bgNhZW0CMTEAAR5BtEA-3IpXHd7eI9290Bu_P-TOSgAhOUnEfg1-uOfewPD7xgx1jBPaJdMMWQ_aem_IO-VzLI0yv-h0O69sOEvqg)

