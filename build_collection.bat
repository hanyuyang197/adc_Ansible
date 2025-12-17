@echo off
REM HORIZON Ansible模块集合构建器 for Windows
REM 此脚本用于构建HORIZON Ansible集合包

echo 正在构建HORIZON Ansible模块集合...

REM 定义变量
set COLLECTION_NAME=horizon-modules
set COLLECTION_VERSION=1.0.0
set BUILD_DIR=build
set COLLECTION_DIR=%BUILD_DIR%\horizon\modules\horizon_modules
set TARBALL_NAME=%COLLECTION_NAME%-%COLLECTION_VERSION%.tar.gz

REM 清理之前的构建
echo 正在清理之前的构建...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%TARBALL_NAME%" del "%TARBALL_NAME%"

REM 创建目录结构
echo 正在创建目录结构...
mkdir "%COLLECTION_DIR%"

REM 复制库模块
echo 正在复制库模块...
mkdir "%COLLECTION_DIR%\plugins\modules"
copy library\*.py "%COLLECTION_DIR%\plugins\modules\" >nul

REM 创建模块工具目录（如果需要）
echo 正在创建模块工具目录...
mkdir "%COLLECTION_DIR%\plugins\module_utils"

REM 复制playbooks（作为示例）
echo 正在复制playbooks...
mkdir "%COLLECTION_DIR%\examples"
copy playbooks\*.yml "%COLLECTION_DIR%\examples\" >nul

REM 创建galaxy.yml文件
echo 正在创建galaxy.yml...
echo namespace: horizon > "%COLLECTION_DIR%\galaxy.yml"
echo name: modules >> "%COLLECTION_DIR%\galaxy.yml"
echo version: %COLLECTION_VERSION% >> "%COLLECTION_DIR%\galaxy.yml"
echo readme: README.md >> "%COLLECTION_DIR%\galaxy.yml"
echo authors: >> "%COLLECTION_DIR%\galaxy.yml"
echo   - Your Name ^<your.email@example.com^> >> "%COLLECTION_DIR%\galaxy.yml"
echo description: 用于ADC（应用交付控制器）管理的Ansible模块 >> "%COLLECTION_DIR%\galaxy.yml"
echo license_file: LICENSE >> "%COLLECTION_DIR%\galaxy.yml"
echo tags: >> "%COLLECTION_DIR%\galaxy.yml"
echo   - adc >> "%COLLECTION_DIR%\galaxy.yml"
echo   - loadbalancer >> "%COLLECTION_DIR%\galaxy.yml"
echo   - networking >> "%COLLECTION_DIR%\galaxy.yml"
echo   - infrastructure >> "%COLLECTION_DIR%\galaxy.yml"
echo dependencies: >> "%COLLECTION_DIR%\galaxy.yml"
echo   ansible_core: "^>=2.9" >> "%COLLECTION_DIR%\galaxy.yml"
echo repository: https://github.com/your-org/horizon-ansible-modules >> "%COLLECTION_DIR%\galaxy.yml"
echo documentation: https://github.com/your-org/horizon-ansible-modules/blob/main/README.md >> "%COLLECTION_DIR%\galaxy.yml"
echo homepage: https://github.com/your-org/horizon-ansible-modules >> "%COLLECTION_DIR%\galaxy.yml"
echo issues: https://github.com/your-org/horizon-ansible-modules/issues >> "%COLLECTION_DIR%\galaxy.yml"
echo build_ignore: >> "%COLLECTION_DIR%\galaxy.yml"
echo   - "*.tar.gz" >> "%COLLECTION_DIR%\galaxy.yml"
echo   - "build" >> "%COLLECTION_DIR%\galaxy.yml"

REM 为集合创建README.md
echo 正在创建README.md...
echo # HORIZON Ansible模块集合 > "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo 此集合提供了用于管理ADC（应用交付控制器）设备的Ansible模块。 >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo ## 包含的模块 >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo - **节点管理**: adc_slb_node, adc_slb_node_port >> "%COLLECTION_DIR%\README.md"
echo - **服务池管理**: adc_slb_pool >> "%COLLECTION_DIR%\README.md"
echo - **健康检查管理**: adc_slb_healthcheck >> "%COLLECTION_DIR%\README.md"
echo - **虚拟地址管理**: adc_slb_va >> "%COLLECTION_DIR%\README.md"
echo - **虚拟服务管理**: adc_slb_va_vs >> "%COLLECTION_DIR%\README.md"
echo - **配置文件管理**: adc_slb_profile_* (fastl4, tcp, udp, http等) >> "%COLLECTION_DIR%\README.md"
echo - 以及更多模块... >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo ## 安装 >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo ```bash >> "%COLLECTION_DIR%\README.md"
echo ansible-galaxy collection install horizon.modules.horizon_modules >> "%COLLECTION_DIR%\README.md"
echo ``` >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo ## 使用方法 >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo ```yaml >> "%COLLECTION_DIR%\README.md"
echo - name: 添加节点 >> "%COLLECTION_DIR%\README.md"
echo   horizon.modules.horizon_modules.adc_slb_node: >> "%COLLECTION_DIR%\README.md"
echo     ip: "192.168.1.100" >> "%COLLECTION_DIR%\README.md"
echo     authkey: "{{ login_result.authkey }}" >> "%COLLECTION_DIR%\README.md"
echo     action: "add_node" >> "%COLLECTION_DIR%\README.md"
echo     name: "test_node" >> "%COLLECTION_DIR%\README.md"
echo     addr: "10.0.0.1" >> "%COLLECTION_DIR%\README.md"
echo     status: 1 >> "%COLLECTION_DIR%\README.md"
echo   register: result >> "%COLLECTION_DIR%\README.md"
echo ``` >> "%COLLECTION_DIR%\README.md"
echo. >> "%COLLECTION_DIR%\README.md"
echo 请参考PACKAGING.md获取详细的安装和使用说明。 >> "%COLLECTION_DIR%\README.md"

REM 创建空的LICENSE文件
echo 正在创建LICENSE文件...
type nul > "%COLLECTION_DIR%\LICENSE"

REM 检查tar是否可用（Git Bash或类似环境）
where tar >nul 2>&1
if %errorlevel% equ 0 (
    REM 使用tar创建tarball
    echo 正在使用tar创建tarball...
    cd "%BUILD_DIR%"
    tar -czf "..\%TARBALL_NAME%" .
    cd ..
) else (
    REM 在Windows上，我们将创建zip文件
    echo 正在创建zip归档...
    powershell.exe -Command "Compress-Archive -Path '%BUILD_DIR%\*' -DestinationPath '%TARBALL_NAME%'"
)

REM 清理构建目录
echo 正在清理...
rmdir /s /q "%BUILD_DIR%"

echo 构建完成！
echo 集合包已创建: %TARBALL_NAME%
echo.
echo 要安装集合，请运行:
echo ansible-galaxy collection install %TARBALL_NAME%