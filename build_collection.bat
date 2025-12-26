@echo off
REM Horizon Modules Ansible 集合包构建脚本 (Windows)

setlocal enabledelayedexpansion

REM 定义变量
set COLLECTION_NAMESPACE=horizon
set COLLECTION_NAME=modules
set COLLECTION_VERSION=1.0.0
set COLLECTION_PACKAGE_NAME=%COLLECTION_NAMESPACE%-%COLLECTION_NAME%-%COLLECTION_VERSION%.tar.gz

echo 开始构建 %COLLECTION_NAMESPACE% %COLLECTION_NAME% 集合包...

REM 创建临时目录
if exist temp_collection_build (
    rmdir /s /q temp_collection_build
)
mkdir temp_collection_build

REM 设置集合目录
set COLLECTION_DIR=temp_collection_build

REM 创建必要的子目录
mkdir "%COLLECTION_DIR%\plugins\modules" 2>nul
mkdir "%COLLECTION_DIR%\meta" 2>nul
mkdir "%COLLECTION_DIR%\docs" 2>nul

REM 检查并复制模块文件
if not exist library (
    echo 错误: 未找到library目录
    rmdir /s /q temp_collection_build
    exit /b 1
)

set MODULE_COUNT=0
for %%f in (library\*.py) do (
    if exist "%%f" (
        copy "%%f" "%COLLECTION_DIR%\plugins\modules\" >nul
        echo 已添加模块: %%~nxf
        set /a MODULE_COUNT+=1
    )
)

if !MODULE_COUNT! EQU 0 (
    echo 错误: library目录中未找到任何.py文件
    rmdir /s /q temp_collection_build
    exit /b 1
)

REM 创建meta/runtime.yml
echo --- > "%COLLECTION_DIR%\meta\runtime.yml"
echo requires_ansible: '>=2.9.10' >> "%COLLECTION_DIR%\meta\runtime.yml"

REM 创建README.md
echo # %COLLECTION_NAMESPACE%.%COLLECTION_NAME% > "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo An Ansible collection for %COLLECTION_NAMESPACE% operations. >> "%COLLECTION_DIR%\README.md"

REM 创建requirements.txt
echo # Collection requirements > "%COLLECTION_DIR%\requirements.txt"

REM 创建临时FILES.json
echo {} > "%COLLECTION_DIR%\FILES.json"

REM 创建MANIFEST.json
echo {" > "%COLLECTION_DIR%\MANIFEST.json"
echo   "collection_info": { >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "namespace": "%COLLECTION_NAMESPACE%", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "name": "%COLLECTION_NAME%", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "version": "%COLLECTION_VERSION%", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "authors": ["Auto-generated"], >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "readme": "README.md", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "tags": ["horizon", "hsm", "monitoring"], >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "description": "Ansible collection for %COLLECTION_NAMESPACE% operations", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "license": ["GPL-3.0-only"], >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "license_file": null, >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "dependencies": {}, >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "repository": null, >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "documentation": null, >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "homepage": null, >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "issues": null >> "%COLLECTION_DIR%\MANIFEST.json"
echo   }, >> "%COLLECTION_DIR%\MANIFEST.json"
echo   "file_manifest_file": { >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "name": "FILES.json", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "ftype": "file", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "chksum_type": "sha256", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "chksum_sha256": "temp-placeholder", >> "%COLLECTION_DIR%\MANIFEST.json"
echo     "format": 1 >> "%COLLECTION_DIR%\MANIFEST.json"
echo   }, >> "%COLLECTION_DIR%\MANIFEST.json"
echo   "format": 1 >> "%COLLECTION_DIR%\MANIFEST.json"
echo } >> "%COLLECTION_DIR%\MANIFEST.json"

REM 使用新的构建脚本生成正确的FILES.json和MANIFEST.json
python build_collection.py

REM 检查Python脚本执行结果
if errorlevel 1 (
    echo Python脚本执行失败
    rmdir /s /q temp_collection_build
    exit /b 1
)

REM 清理临时目录
rmdir /s /q temp_collection_build

echo 构建完成: %COLLECTION_PACKAGE_NAME%
for %%A in (%COLLECTION_PACKAGE_NAME%) do echo 包大小: %%~zA bytes

echo.
echo 集合包构建成功！
