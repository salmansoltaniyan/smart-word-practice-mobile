#!/bin/bash
# One-command APK builder for Google Colab

echo "📱 Smart Word Practice - One Command APK Builder"
echo "=============================================="

# Exit on any error
set -e

# Function to handle errors
handle_error() {
    echo "❌ Build failed at step: $1"
    echo "💡 Try GitHub Codespaces instead: https://github.com/salmansoltaniyan/smart-word-practice-mobile"
    exit 1
}

# Step 1: System setup
echo "🔧 Step 1/6: System setup..."
apt-get update -qq || handle_error "System update"
apt-get install -y openjdk-8-jdk build-essential git unzip || handle_error "Installing system packages"

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Step 2: Clone repository
echo "📥 Step 2/6: Getting source code..."
if [ ! -d "smart-word-practice-mobile" ]; then
    git clone https://github.com/salmansoltaniyan/smart-word-practice-mobile.git || handle_error "Cloning repository"
fi
cd smart-word-practice-mobile

# Step 3: Python dependencies with retries
echo "🐍 Step 3/6: Installing Python packages..."
pip install --upgrade pip setuptools wheel || handle_error "Upgrading pip"

# Try multiple Kivy installation methods
echo "  Installing Kivy..."
pip install kivy==2.2.0 || \
pip install kivy==2.1.0 || \
pip install kivy || \
handle_error "Installing Kivy"

echo "  Installing Buildozer..."
pip install buildozer || handle_error "Installing Buildozer"

echo "  Installing Requests..."
pip install requests || handle_error "Installing Requests"

# Step 4: Verify setup
echo "✅ Step 4/6: Verifying installation..."
python3 -c "import kivy; print('Kivy OK')" || handle_error "Kivy verification"
python3 -c "import buildozer; print('Buildozer OK')" || handle_error "Buildozer verification"

# Step 5: Build APK
echo "🚀 Step 5/6: Building APK (15-20 minutes)..."
echo "☕ Grab a coffee! This takes a while..."

timeout 30m buildozer android debug || handle_error "APK build (timeout or error)"

# Step 6: Check results
echo "🎉 Step 6/6: Checking results..."
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo "✅ SUCCESS! APK built successfully:"
    ls -lh bin/*.apk
    echo ""
    echo "📱 Your Android app is ready!"
    echo "📁 Download from: smart-word-practice-mobile/bin/"
else
    handle_error "No APK file found"
fi