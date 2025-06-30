@echo off
echo 正在清理 mock_dataset 下所有测试生成文件夹和非 .md 文件（保留报告）...

REM 批量删除 mock_dataset 下除 .md 外的所有子文件夹
for /d %%i in (mock_dataset\*) do (
    echo 删除文件夹：%%i
    rmdir /s /q "%%i"
)

REM 批量删除 mock_dataset 下除 .md 外的所有单文件
for %%f in (mock_dataset\*) do (
    if /I not "%%~xf"==".md" (
        echo 删除文件：%%f
        del /f /q "%%f"
    )
)

echo 清理完成 ?
pause
