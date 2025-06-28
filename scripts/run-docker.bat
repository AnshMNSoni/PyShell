@echo off
chcp 65001 >nul

echo 🐍 PyShell Terminal - Docker Edition
echo =====================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Function to build and run
:build_and_run
echo 🔨 Building PyShell Docker image...
docker-compose build
if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)
echo ✅ Build successful!
echo 🚀 Starting PyShell Terminal...
echo 💡 Tip: Use 'exit' command to quit the terminal
echo.
docker-compose run --rm pyshell
goto :eof

REM Function to just run (if already built)
:run_only
echo 🚀 Starting PyShell Terminal...
echo 💡 Tip: Use 'exit' command to quit the terminal
echo.
docker-compose run --rm pyshell
goto :eof

REM Function to clean up
:cleanup
echo 🧹 Cleaning up Docker resources...
docker-compose down
docker system prune -f
echo ✅ Cleanup complete!
pause
goto :eof

REM Main menu
if "%1"=="build" goto build_and_run
if "%1"=="run" goto run_only
if "%1"=="clean" goto cleanup
if "%1"=="rebuild" (
    call :cleanup
    goto build_and_run
)

REM Default action
if "%1"=="" goto build_and_run

echo Usage: %0 {build^|run^|clean^|rebuild}
echo.
echo Commands:
echo   build   - Build and run PyShell (default^)
echo   run     - Run PyShell (assumes already built^)
echo   clean   - Clean up Docker resources
echo   rebuild - Clean and rebuild everything
pause
exit /b 1 