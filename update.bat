@echo off
:: 获取拖拽的文件或文件夹路径
set "drag_path=%~1"
:: 切换到项目目录
cd /d "%~dp1"
:: 执行Git操作
git add .
git commit -m "Your commit message"
git push origin main
pause