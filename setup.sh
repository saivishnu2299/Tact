#!/bin/bash
# Tact Haptic Feedback System - Setup Script
# This script creates a virtual environment and installs dependencies

set -e  # Exit on any error

echo "Tact Haptic Feedback System - Setup"
echo "====================================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "   Please install Python 3 and try again"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r host-app/requirements.txt

echo
echo "🎉 Setup complete!"
echo
echo "To use the Tact system:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Upload firmware to Arduino 101: firmware/tact_haptic_controller.ino"
echo "3. Run the host simulator: python host-app/tact_host_simulator.py --test"
echo "4. Try interactive mode: python host-app/tact_host_simulator.py --interactive"
echo
echo "For detailed instructions, see README.md"