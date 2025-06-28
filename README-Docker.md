# PyShell Terminal - Docker Setup Guide

## 🐳 Docker Benefits

### ✅ **Consistency Across Environments**
- **Same environment everywhere**: Whether you're on Windows, macOS, or Linux, Docker ensures the exact same Python version, dependencies, and system libraries.
- **No "works on my machine" issues**: Eliminates environment-specific bugs and configuration problems.
- **Reproducible builds**: Exact same container runs identically everywhere.

### ✅ **Easy Setup & Deployment**
- **One-command installation**: No need to manually install Python, pip, or manage virtual environments.
- **Dependency isolation**: All required packages are bundled together without conflicts.
- **Quick onboarding**: New team members can start immediately with `docker-compose up`.

### ✅ **System Independence**
- **No local Python installation required**: Docker handles all Python dependencies.
- **Clean system**: No pollution of your local Python environment.
- **Version control**: Exact Python and package versions are locked in the container.

### ✅ **Professional Features**
- **Security**: Runs as non-root user with minimal attack surface.
- **Scalability**: Easy to deploy multiple instances.
- **Production ready**: Optimized for deployment and sharing.

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git (to clone the repository)

### Method 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/AnshMNSoni/PyShell.git
cd PyShell

# Build and run with one command
docker-compose up --build
```

### Method 2: Using Convenience Scripts

#### On Windows:
```cmd
# Run PyShell
scripts\run-docker.bat

# Or with specific commands
scripts\run-docker.bat build    # Build and run
scripts\run-docker.bat run      # Run only (if already built)
scripts\run-docker.bat clean    # Clean up Docker resources
scripts\run-docker.bat rebuild  # Clean and rebuild everything
```

#### On Linux/macOS:
```bash
# Make script executable
chmod +x scripts/run-docker.sh

# Run PyShell
./scripts/run-docker.sh

# Or with specific commands
./scripts/run-docker.sh build    # Build and run
./scripts/run-docker.sh run      # Run only (if already built)
./scripts/run-docker.sh clean    # Clean up Docker resources
./scripts/run-docker.sh rebuild  # Clean and rebuild everything
```

### Method 3: Using Automated Setup Script

```bash
# Run the smart setup script
python setup.py

# The script will:
# 1. Detect if Docker is available
# 2. Offer Docker or traditional setup
# 3. Handle all configuration automatically
```

### Method 4: Manual Docker Commands

```bash
# Build the image
docker build -t pyshell-terminal .

# Run the container
docker run -it --rm pyshell-terminal

# Run with volume mounts for development
docker run -it --rm -v $(pwd):/app pyshell-terminal
```

## 📁 Volume Mounts & Data Persistence

The Docker setup includes several volume mounts for data persistence:

### **User Data:**
- **`./users.json`** → User authentication data (encrypted passwords)
- **`./high_score.txt`** → Global high scores

### **Game Data:**
- **`./game/Ping-Pong/high_score.txt`** → Ping-Pong game scores
- **`./game/Snake-Game/high-score.txt`** → Snake game scores

### **Development Mounts:**
- **`.:/app`** → Entire project directory for live development

This ensures your data persists between container restarts and updates.

## 🔧 Configuration

### Environment Variables
You can customize the behavior by setting environment variables:

```yaml
# In docker-compose.yml
environment:
  - PYTHONPATH=/app
  - PYTHONUNBUFFERED=1
  - DISPLAY=${DISPLAY}  # For GUI features (Linux/macOS)
```

### Custom Requirements
To add new dependencies:

1. Add them to `requirements.txt`
2. Rebuild the container: `docker-compose build`

### Port Configuration
For web features (if added in future):

```yaml
# Add to docker-compose.yml
ports:
  - "5000:5000"  # Host port : Container port
```

## 🎮 Features That Work in Docker

### ✅ Fully Supported
- All CLI commands and utilities
- File operations and process management
- Weather API integration
- Task scheduling and Git operations
- Mathematical calculations and graphing
- Password generation and clipboard operations
- User authentication with SHA-256 encryption
- All terminal layouts and themes

### ⚠️ Partially Supported
- **Audio playback**: May require additional audio setup on some systems
- **GUI games**: Some games may have limited functionality in headless mode

### 🔧 Audio Setup (Optional)
For audio features, you may need to mount audio devices:

```yaml
# Add to docker-compose.yml
volumes:
  - /dev/snd:/dev/snd  # Linux audio devices
  - /tmp/.X11-unix:/tmp/.X11-unix  # X11 for GUI (Linux)
```

## 🛠️ Development Workflow

### Making Changes
1. Edit your code locally
2. Changes are immediately reflected due to volume mounting
3. Restart the container if needed: `docker-compose restart`

### Debugging
```bash
# Run with debug output
docker-compose run --rm pyshell python -u main.py

# Access container shell
docker-compose run --rm pyshell /bin/bash

# View logs
docker-compose logs pyshell
```

### Building for Production
```bash
# Build optimized production image
docker build -t pyshell-terminal:prod --target production .

# Run production container
docker run -d --name pyshell-prod pyshell-terminal:prod
```

## 🧹 Maintenance

### Cleanup Commands
```bash
# Remove containers and networks
docker-compose down

# Remove images
docker rmi pyshell-terminal

# Clean up all unused Docker resources
docker system prune -a

# Remove specific volumes
docker volume rm pyshell_users_data
```

### Updating Dependencies
1. Update `requirements.txt`
2. Rebuild: `docker-compose build --no-cache`
3. Test the new version

### Monitoring
```bash
# Check container status
docker-compose ps

# View resource usage
docker stats pyshell-terminal

# Check container logs
docker-compose logs -f pyshell
```

## 🔒 Security Considerations

### Container Security
- **Non-root user**: Container runs as user `pyshell` (UID 1000)
- **Minimal base image**: Uses Python slim image to reduce attack surface
- **No unnecessary packages**: Only required system dependencies are installed
- **Volume isolation**: User data is properly isolated

### Password Security
- **SHA-256 encryption**: All passwords are hashed using SHA-256
- **No plain text storage**: Passwords are never stored in plain text
- **Automatic migration**: Existing passwords are automatically encrypted
- **Secure comparison**: Password verification uses constant-time comparison

### Network Security
- **No exposed ports**: Container doesn't expose unnecessary ports
- **Internal networking**: Uses Docker's internal network isolation
- **No root access**: Container cannot access host system

## 🐛 Troubleshooting

### Common Issues

#### Docker not running
```bash
# Start Docker Desktop or Docker daemon
sudo systemctl start docker  # Linux
# Or start Docker Desktop application
```

#### Permission issues
```bash
# Fix file permissions
chmod +x scripts/run-docker.sh

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

#### Port conflicts
```yaml
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different host port
```

#### Audio not working
```bash
# Install pulseaudio (Linux)
sudo apt-get install pulseaudio

# Or use ALSA
docker run --device /dev/snd pyshell-terminal
```

#### Git commands not working
```bash
# Git is included in the Dockerfile
# If issues persist, check container logs
docker-compose logs pyshell
```

#### Password authentication issues
```bash
# Check if users.json exists and has proper format
cat users.json

# Reset user data if needed
rm users.json
docker-compose run --rm pyshell
```

### Getting Help
1. **Check Docker logs**: `docker-compose logs`
2. **Verify container status**: `docker-compose ps`
3. **Access container shell**: `docker-compose exec pyshell /bin/bash`
4. **Check system resources**: `docker system df`

## 📊 Performance Comparison

| Aspect | Traditional Setup | Docker Setup |
|--------|------------------|--------------|
| **Setup Time** | 10-15 minutes | 2-3 minutes |
| **Dependency Management** | Manual/venv | Automated |
| **Environment Consistency** | Variable | Guaranteed |
| **System Impact** | High (global installs) | Low (isolated) |
| **Deployment** | Complex | Simple |
| **Rollback** | Difficult | Easy |
| **Sharing** | Manual instructions | One command |

## 🎯 Use Cases

### For Individual Users
- **Quick setup**: Get PyShell running in minutes
- **No system pollution**: Keep your system clean
- **Easy cleanup**: Remove everything with one command

### For Teams
- **Consistent environment**: Same setup for all team members
- **Easy onboarding**: New developers can start immediately
- **Version control**: Exact same versions everywhere

### For Production
- **Deployment ready**: Easy to deploy to any server
- **Scalable**: Can run multiple instances
- **Secure**: Isolated environment with security best practices

### For Development
- **Live development**: Changes reflect immediately
- **Debugging**: Easy access to container shell
- **Testing**: Consistent test environment

## 🔄 Migration from Traditional Setup

### For Existing Users
1. **No data loss**: Your user data and high scores are preserved
2. **Automatic migration**: Passwords are automatically encrypted
3. **Same functionality**: All features work exactly the same

### Migration Steps
1. **Backup your data** (optional but recommended)
2. **Install Docker Desktop**
3. **Run Docker setup**: `docker-compose up --build`
4. **Login with existing credentials**

## 🚀 Advanced Usage

### Custom Dockerfile
```dockerfile
# Example: Add custom dependencies
FROM pyshellterminal-pyshell:latest

# Install additional packages
RUN apt-get update && apt-get install -y \
    your-package \
    another-package

# Copy custom configuration
COPY custom-config.py /app/
```

### Docker Compose Override
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  pyshell:
    environment:
      - DEBUG=true
      - CUSTOM_SETTING=value
    volumes:
      - ./custom-data:/app/custom-data
```

### Multi-Stage Build
```dockerfile
# Development stage
FROM python:3.11-slim as development
# ... development setup

# Production stage
FROM python:3.11-slim as production
# ... production setup
```

## 📝 Best Practices

### Development
- **Use volume mounts** for live development
- **Check logs regularly** for debugging
- **Keep Docker images updated**
- **Use .dockerignore** to optimize builds

### Production
- **Use specific image tags** instead of `latest`
- **Implement health checks**
- **Monitor resource usage**
- **Regular security updates**

### Security
- **Never run as root** in containers
- **Use minimal base images**
- **Scan images for vulnerabilities**
- **Keep secrets out of images**

## 🎉 Conclusion

Docker provides a modern, reliable way to run PyShell Terminal with:
- **Faster setup** and **easier maintenance**
- **Consistent behavior** across different systems
- **Better isolation** and **security**
- **Simplified deployment** and **scaling**

The Docker setup is especially beneficial for:
- **New users** who want to try PyShell quickly
- **Developers** working on different machines
- **Teams** that need consistent environments
- **Production deployments** requiring reliability

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your system meets the requirements
3. Try the automated setup script first
4. Check the project issues on GitHub
5. Review Docker documentation for your platform

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Docker Images](https://hub.docker.com/_/python)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Happy containerizing! 🐳** 