#!/usr/bin/env python3
"""
PyShell Terminal Setup Script
Automated setup for both Docker and traditional installation
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class PyShellSetup:
    def __init__(self):
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        self.is_linux = self.system == "Linux"
        self.is_macos = self.system == "Darwin"
        
    def print_banner(self):
        """Print the PyShell banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🐍 PyShell Terminal Setup                ║
║                                                              ║
║  Automated setup for Docker and traditional installation     ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8 or higher is required!")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def check_docker(self):
        """Check if Docker is installed and running"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Docker is installed")
                # Check if Docker daemon is running
                try:
                    subprocess.run(['docker', 'info'], 
                                  capture_output=True, text=True, timeout=5)
                    print("✅ Docker daemon is running")
                    return True
                except subprocess.TimeoutExpired:
                    print("⚠️  Docker is installed but daemon is not running")
                    return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Docker is not installed or not accessible")
            return False
    
    def install_docker_windows(self):
        """Provide instructions for Docker installation on Windows"""
        print("\n🔧 Docker Installation Instructions for Windows:")
        print("=" * 50)
        print("1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        print("2. Run the installer and follow the setup wizard")
        print("3. Restart your computer if prompted")
        print("4. Start Docker Desktop from the Start menu")
        print("5. Wait for Docker to finish starting up")
        print("6. Run this setup script again")
        print("\n💡 Alternative: Use traditional installation (no Docker required)")
        
        choice = input("\nWould you like to proceed with traditional installation? (y/n): ").lower()
        return choice == 'y'
    
    def install_dependencies_traditional(self):
        """Install dependencies using pip"""
        print("\n📦 Installing Python dependencies...")
        
        # Check if pip is available
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("❌ pip is not available. Please install pip first.")
            return False
        
        # Upgrade pip
        print("🔄 Upgrading pip...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                          check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not upgrade pip: {e}")
        
        # Install requirements
        print("📥 Installing requirements from requirements.txt...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                          check=True)
            print("✅ All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_virtual_environment(self):
        """Create a virtual environment"""
        venv_path = Path("venv")
        if venv_path.exists():
            print("✅ Virtual environment already exists")
            return True
        
        print("🔧 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print("✅ Virtual environment created successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def setup_docker(self):
        """Setup and run with Docker"""
        print("\n🐳 Setting up Docker environment...")
        
        # Build Docker image
        print("🔨 Building Docker image...")
        try:
            subprocess.run(['docker-compose', 'build'], check=True)
            print("✅ Docker image built successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Docker image: {e}")
            return False
        
        # Run the container
        print("🚀 Starting PyShell Terminal with Docker...")
        try:
            subprocess.run(['docker-compose', 'run', '--rm', 'pyshell'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run Docker container: {e}")
            return False
    
    def run_traditional(self):
        """Run PyShell in traditional mode"""
        print("\n🚀 Starting PyShell Terminal...")
        print("💡 Tip: Use 'exit' command to quit the terminal")
        print("=" * 50)
        
        try:
            subprocess.run([sys.executable, 'main.py'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run PyShell: {e}")
            return False
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return True
    
    def create_launch_scripts(self):
        """Create convenient launch scripts"""
        if self.is_windows:
            # Windows batch file (without emoji to avoid encoding issues)
            batch_content = """@echo off
echo Starting PyShell Terminal...
python main.py
pause
"""
            with open("run-pyshell.bat", "w", encoding="utf-8") as f:
                f.write(batch_content)
            print("✅ Created run-pyshell.bat")
        else:
            # Unix shell script
            shell_content = """#!/bin/bash
echo "🐍 Starting PyShell Terminal..."
python3 main.py
"""
            with open("run-pyshell.sh", "w") as f:
                f.write(shell_content)
            os.chmod("run-pyshell.sh", 0o755)
            print("✅ Created run-pyshell.sh")
    
    def main(self):
        """Main setup function"""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return
        
        print(f"\n🖥️  Operating System: {self.system}")
        
        # Check if Docker is available
        docker_available = self.check_docker()
        
        if docker_available:
            print("\n🎯 Setup Options:")
            print("1. 🐳 Docker Setup (Recommended)")
            print("2. 📦 Traditional Setup")
            
            choice = input("\nChoose setup method (1/2): ").strip()
            
            if choice == "1":
                if self.setup_docker():
                    print("✅ Docker setup completed successfully!")
                else:
                    print("❌ Docker setup failed. Falling back to traditional setup...")
                    self.install_dependencies_traditional()
                    self.create_launch_scripts()
                    self.run_traditional()
            else:
                self.install_dependencies_traditional()
                self.create_launch_scripts()
                self.run_traditional()
        else:
            print("\n🐳 Docker is not available.")
            if self.is_windows:
                if not self.install_docker_windows():
                    print("👋 Setup cancelled.")
                    return
            
            print("\n📦 Proceeding with traditional installation...")
            if self.install_dependencies_traditional():
                self.create_launch_scripts()
                self.run_traditional()
            else:
                print("❌ Traditional setup failed!")

if __name__ == "__main__":
    setup = PyShellSetup()
    setup.main() 