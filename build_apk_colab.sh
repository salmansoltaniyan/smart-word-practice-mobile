#!/bin/bash
# Smart Word Practice - APK Builder for Google Colab (Fixed Version)

echo "📱 Smart Word Practice - APK Builder (Colab Optimized)"
echo "=================================================="

# Clone the repository
echo "📥 Cloning repository..."
if [ ! -d "smart-word-practice-mobile" ]; then
    git clone https://github.com/salmansoltaniyan/smart-word-practice-mobile.git
fi
cd smart-word-practice-mobile

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update -qq
apt-get install -y openjdk-8-jdk build-essential git unzip wget curl
apt-get install -y python3-pip python3-dev python3-setuptools
apt-get install -y libffi-dev libssl-dev zlib1g-dev libbz2-dev
apt-get install -y libreadline-dev libsqlite3-dev libncurses5-dev
apt-get install -y libncursesw5-dev xz-utils tk-dev

# Set Java home
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Install Cython first (required for Kivy)
echo "🐍 Installing Cython..."
pip install --upgrade pip setuptools wheel
pip install cython==0.29.33

# Install Kivy with pre-built wheel (avoid compilation)
echo "🎨 Installing Kivy..."
pip install kivy==2.2.0 --only-binary=all

# Install buildozer
echo "� Installing Buildozer..."
pip install buildozer

# Install other dependencies
echo "📦 Installing other dependencies..."
pip install requests

# Verify installations
echo "✅ Verifying installations..."
python3 -c "import kivy; print(f'Kivy version: {kivy.__version__}')" || echo "❌ Kivy failed"
python3 -c "import buildozer; print('✅ Buildozer installed')" || echo "❌ Buildozer failed"
python3 -c "import requests; print('✅ Requests installed')" || echo "❌ Requests failed"

# Add pip binaries to PATH
export PATH=$PATH:~/.local/bin
export PATH=$PATH:/usr/local/bin

# Check if buildozer is accessible
which buildozer || echo "❌ Buildozer not in PATH"

# Initialize buildozer (this may take time on first run)
echo "🚀 Initializing Buildozer..."
buildozer init || echo "⚠️ Init failed, continuing..."

# Build APK
echo "� Building APK (this will take ~15-20 minutes)..."
buildozer android debug || echo "❌ Build failed"

# Show results
echo "✅ Build process complete!"
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo "🎉 APK files created successfully:"
    ls -la bin/*.apk
    echo ""
    echo "📁 To download:"
    echo "   1. Go to Files panel on the left"
    echo "   2. Navigate to smart-word-practice-mobile/bin/"
    echo "   3. Right-click the .apk file"
    echo "   4. Click Download"
else
    echo "❌ No APK files found. Possible issues:"
    echo "   • Check the build log above for specific errors"
    echo "   • Buildozer may need more system resources"
    echo "   • Try using GitHub Codespaces instead"
fi