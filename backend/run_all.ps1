# 進入 backend 目錄
Set-Location $PSScriptRoot

# 啟動 FastAPI 服務（背景執行）
$server = Start-Process -FilePath "poetry" -ArgumentList "run", "uvicorn", "main:app", "--reload" -PassThru

# 等待服務啟動
Start-Sleep -Seconds 5

# 執行 pytest 測試
poetry run pytest tests

# 測試結束後自動關閉 FastAPI 服務
Stop-Process -Id $server.Id 