#!/bin/bash
# Imagen4 Setup Script for Unix-like systems

# Set text colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=======================================================${NC}"
echo -e "${YELLOW}          Imagen4 CLI Setup Helper Script              ${NC}"
echo -e "${YELLOW}=======================================================${NC}"

# Check if Python is installed
echo -e "\n${YELLOW}Checking Python installation...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Python not found. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_VERSION_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_VERSION_MAJOR" -lt 3 ] || ([ "$PYTHON_VERSION_MAJOR" -eq 3 ] && [ "$PYTHON_VERSION_MINOR" -lt 7 ]); then
    echo -e "${RED}Python 3.7 or higher is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}Python $PYTHON_VERSION found.${NC}"

# Check if gcloud is installed
echo -e "\n${YELLOW}Checking Google Cloud SDK installation...${NC}"
if ! command -v gcloud &>/dev/null; then
    echo -e "${RED}Google Cloud SDK (gcloud) not found.${NC}"
    echo -e "Please install the Google Cloud SDK from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}Google Cloud SDK found.${NC}"

# Check if virtual environment should be created
echo -e "\n${YELLOW}Do you want to create a virtual environment? (recommended) [Y/n]${NC}"
read -r CREATE_VENV
CREATE_VENV=${CREATE_VENV:-Y}

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    
    # Check if venv module is available
    if ! $PYTHON_CMD -c "import venv" &>/dev/null; then
        echo -e "${RED}Python venv module not found. Please install it first.${NC}"
        echo -e "For Ubuntu/Debian: sudo apt-get install python3-venv"
        echo -e "For Fedora: sudo dnf install python3-venv"
        echo -e "For macOS: brew install python3"
        exit 1
    fi
    
    # Create and activate virtual environment
    $PYTHON_CMD -m venv venv
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo -e "${GREEN}Virtual environment created and activated.${NC}"
    else
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Run the Python setup script
echo -e "\n${YELLOW}Running setup script...${NC}"
$PYTHON_CMD setup.py

# Check if setup was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Setup completed successfully!${NC}"
    
    # Source the .env file if it exists
    if [ -f ".env" ]; then
        echo -e "\n${YELLOW}Loading environment variables from .env file...${NC}"
        export $(grep -v '^#' .env | xargs)
        echo -e "${GREEN}Environment variables loaded.${NC}"
    fi
    
    echo -e "\n${YELLOW}You can now run the Imagen4 CLI:${NC}"
    echo -e "${GREEN}$PYTHON_CMD imagen4_cli.py --prompt \"Your creative prompt here\"${NC}"
else
    echo -e "\n${RED}Setup failed. Please check the error messages above.${NC}"
    exit 1
fi

