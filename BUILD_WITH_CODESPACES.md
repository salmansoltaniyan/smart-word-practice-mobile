# Smart Word Practice - Codespaces APK Builder

## 🚀 Build APK using GitHub Codespaces (Free!)

### Steps:

1. **Open your repository:** https://github.com/salmansoltaniyan/smart-word-practice-mobile

2. **Click the green "Code" button** → **"Codespaces" tab** → **"Create codespace on master"**

3. **Wait for Codespace to load** (Ubuntu environment with VS Code)

4. **In the Codespace terminal, run these commands:**

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential git unzip openjdk-8-jdk
sudo apt-get install -y python3-pip python3-dev libffi-dev libssl-dev

# Install Python dependencies
pip install buildozer cython==0.29.33 kivy[base]==2.2.0 requests

# Build the APK
buildozer android debug
```

5. **Download the APK:**
   - The APK will be created in the `bin/` folder
   - Right-click the APK file → "Download"
   - Or use: `zip -r my-app.zip bin/` then download the zip

### ⏱️ Build Time: ~15-20 minutes
### 💰 Cost: Free (120 hours/month)
### 🎯 Success Rate: Very High

---

## Alternative: Use the Commands Below in Codespaces Terminal

```bash
#!/bin/bash
echo "🚀 Building Smart Word Practice APK..."

# Update system
sudo apt-get update -qq

# Install Java 8 (required for Android builds)
sudo apt-get install -y openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Install build dependencies
sudo apt-get install -y build-essential git unzip wget
sudo apt-get install -y python3-pip python3-dev python3-setuptools
sudo apt-get install -y libffi-dev libssl-dev zlib1g-dev
sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev
sudo apt-get install -y libncurses5-dev libncursesw5-dev xz-utils tk-dev

# Install Python packages
pip3 install --user buildozer cython==0.29.33
pip3 install --user 'kivy[base]==2.2.0'
pip3 install --user requests

# Add local pip to PATH
export PATH=$PATH:~/.local/bin

# Build APK
echo "📱 Starting APK build..."
buildozer android debug

# Check result
if [ -f "bin/*.apk" ]; then
    echo "✅ APK built successfully!"
    ls -la bin/
    echo "📁 Download your APK from the bin/ folder"
else
    echo "❌ APK build failed. Check the output above for errors."
fi
```