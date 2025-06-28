# PyShell Terminal - Installation Guide

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
python setup.py
```

This script will:
- ✅ Check your system requirements
- ✅ Detect if Docker is available
- ✅ Install dependencies automatically
- ✅ Create convenient launch scripts
- ✅ Start PyShell Terminal

### Option 2: Manual Installation

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 2GB RAM
- **Storage**: 500MB free space

### For Docker Setup (Optional)
- **Docker Desktop**: Latest version
- **Docker Compose**: Usually included with Docker Desktop

## 🐳 Docker Installation

### Windows
1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Choose Windows 10/11 version

2. **Install Docker Desktop**
   - Run the downloaded installer
   - Follow the installation wizard
   - Restart your computer if prompted

3. **Start Docker Desktop**
   - Open Docker Desktop from Start menu
   - Wait for Docker to finish starting (whale icon in system tray)
   - Accept terms and conditions

4. **Verify Installation**
   ```cmd
   docker --version
   docker-compose --version
   ```

### macOS
1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Mac"
   - Choose Intel or Apple Silicon version

2. **Install Docker Desktop**
   - Drag Docker to Applications folder
   - Open Docker from Applications
   - Follow the setup wizard

3. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker-compose --version
```

## 📦 Traditional Installation

### Step 1: Install Python
1. **Download Python**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**
   ```bash
   python --version
   pip --version
   ```

### Step 2: Clone Repository
```bash
git clone https://github.com/AnshMNSoni/PyShell.git
cd PyShell
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Run PyShell
```bash
python main.py
```

## 🎯 Installation Methods Comparison

| Method | Setup Time | Dependencies | Isolation | Ease of Use |
|--------|------------|--------------|-----------|-------------|
| **Automated Script** | 2-3 min | Automatic | Good | ⭐⭐⭐⭐⭐ |
| **Docker** | 5-10 min | Automatic | Excellent | ⭐⭐⭐⭐ |
| **Traditional** | 10-15 min | Manual | Poor | ⭐⭐⭐ |

## 🐳 Docker Setup (Once Docker is Installed)

### Quick Docker Commands
```bash
# Build and run with one command
docker-compose up --build

# Run only (if already built)
docker-compose run --rm pyshell

# Clean up
docker-compose down
docker system prune -f
```

### Using Convenience Scripts
```bash
# Windows
scripts\run-docker.bat

# Linux/macOS
./scripts/run-docker.sh
```

### Docker Benefits
- ✅ **No Python installation required**
- ✅ **Consistent environment everywhere**
- ✅ **Automatic dependency management**
- ✅ **Isolated from your system**
- ✅ **Easy setup and cleanup**

## 🔧 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows: Add Python to PATH
# Or use full path
C:\Python39\python.exe main.py

# Linux/macOS: Use python3
python3 main.py
```

#### Permission Errors (Linux/macOS)
```bash
# Fix permissions
chmod +x scripts/run-docker.sh
chmod +x run-pyshell.sh
```

#### Docker Permission Errors
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Windows: Run Docker Desktop as Administrator
```

#### Port Conflicts
```yaml
# Edit docker-compose.yml
ports:
  - "5001:5000"  # Use different host port
```

#### Audio Issues (Docker)
```bash
# Linux: Install pulseaudio
sudo apt-get install pulseaudio

# Or use ALSA
docker run --device /dev/snd pyshell-terminal
```

### Dependency Issues

#### pygame Installation Fails
```bash
# Windows: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Linux: Install development packages
sudo apt-get install python3-dev libasound2-dev
```

#### psutil Installation Fails
```bash
# Windows: Install Visual C++ Build Tools
# Linux: Install python3-dev
sudo apt-get install python3-dev
```

### Getting Help
1. **Check logs**: `docker-compose logs`
2. **Verify container**: `docker-compose ps`
3. **Access shell**: `docker-compose exec pyshell /bin/bash`
4. **Check Python**: `python --version`
5. **Check pip**: `pip --version`

## 🎮 Features That Work

### ✅ Fully Supported
- All CLI commands and utilities
- File operations and process management
- Weather API integration
- Task scheduling and Git operations
- Mathematical calculations and graphing
- Password generation and clipboard operations

### ⚠️ Partially Supported (Docker)
- **Audio playback**: May require additional setup
- **GUI games**: Limited functionality in headless mode

## 📁 Project Structure
```
Pyshell terminal/
├── main.py              # Main application
├── setup.py             # Automated setup script
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker orchestration
├── scripts/            # Convenience scripts
│   ├── run-docker.bat  # Windows Docker runner
│   └── run-docker.sh   # Linux/macOS Docker runner
├── game/               # Game modules
├── users.json          # User data (created on first run)
└── README.md           # Project documentation
```

## 🚀 Next Steps

1. **Run the setup script**: `python setup.py`
2. **Choose your preferred method**: Docker or Traditional
3. **Follow the prompts**: The script will guide you through setup
4. **Start using PyShell**: Enjoy your new terminal experience!

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your system meets the requirements
3. Try the automated setup script first
4. Check the project issues on GitHub