#!/bin/bash
# Smart Word Practice - APK Builder for Google Colab

echo "📱 Smart Word Practice - APK Builder"
echo "=================================="

# Clone the repository
echo "📥 Cloning repository..."
git clone https://github.com/salmansoltaniyan/smart-word-practice-mobile.git
cd smart-word-practice-mobile

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update -qq
apt-get install -y openjdk-8-jdk build-essential git unzip wget
apt-get install -y python3-pip python3-dev libffi-dev libssl-dev

# Set Java home
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install buildozer cython==0.29.33 'kivy[base]==2.2.0' requests

# Build APK
echo "🚀 Building APK (this will take ~10-15 minutes)..."
buildozer android debug

# Show results
echo "✅ Build complete!"
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo "📱 APK files created:"
    ls -la bin/*.apk
    echo ""
    echo "📁 To download: Right-click on APK file in file browser → Download"
else
    echo "❌ No APK files found. Check build output for errors."
fi