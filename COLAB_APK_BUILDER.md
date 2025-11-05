# 📱 Smart Word Practice - Google Colab APK Builder

## Run each cell step by step. Total time: ~20-25 minutes

### Step 1: Setup Environment
```python
import os
import subprocess
import sys

def run_command(cmd, description=""):
    print(f"🔧 {description}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    else:
        print(f"✅ Success: {description}")
        return True

# Update system and install Java
print("📦 Installing system dependencies...")
run_command("apt-get update -qq", "Updating packages")
run_command("apt-get install -y openjdk-8-jdk build-essential git unzip wget", "Installing Java and build tools")

# Set environment variables
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['JAVA_HOME'] + '/bin'

print("✅ Environment setup complete!")
```

### Step 2: Clone Repository
```python
# Clone the app repository
if not os.path.exists('smart-word-practice-mobile'):
    run_command("git clone https://github.com/salmansoltaniyan/smart-word-practice-mobile.git", "Cloning repository")
    
os.chdir('smart-word-practice-mobile')
print("📁 Current directory:", os.getcwd())
print("📋 Files in directory:")
for file in os.listdir('.'):
    print(f"  - {file}")
```

### Step 3: Install Python Dependencies
```python
# Install dependencies step by step
print("🐍 Installing Python dependencies...")

# Upgrade pip first
run_command("pip install --upgrade pip setuptools wheel", "Upgrading pip")

# Install Cython (required for Kivy)
run_command("pip install cython==0.29.33", "Installing Cython")

# Install Kivy with binary wheel (avoid compilation)
run_command("pip install kivy==2.2.0", "Installing Kivy")

# Install buildozer
run_command("pip install buildozer", "Installing Buildozer")

# Install requests
run_command("pip install requests", "Installing Requests")

print("✅ All Python packages installed!")
```

### Step 4: Verify Installation
```python
# Test imports
try:
    import kivy
    print(f"✅ Kivy {kivy.__version__} imported successfully")
except ImportError as e:
    print(f"❌ Kivy import failed: {e}")

try:
    import buildozer
    print("✅ Buildozer imported successfully")
except ImportError as e:
    print(f"❌ Buildozer import failed: {e}")

try:
    import requests
    print("✅ Requests imported successfully")
except ImportError as e:
    print(f"❌ Requests import failed: {e}")

# Check if buildozer command is available
result = subprocess.run("which buildozer", shell=True, capture_output=True, text=True)
if result.returncode == 0:
    print(f"✅ Buildozer command found at: {result.stdout.strip()}")
else:
    print("❌ Buildozer command not found in PATH")
```

### Step 5: Build APK
```python
import time

print("🚀 Starting APK build process...")
print("⏰ This will take approximately 15-20 minutes")
print("☕ Perfect time for a coffee break!")

start_time = time.time()

# Run buildozer android debug
result = subprocess.run("buildozer android debug", shell=True, text=True)

end_time = time.time()
build_time = (end_time - start_time) / 60

print(f"⏰ Build completed in {build_time:.1f} minutes")

if result.returncode == 0:
    print("✅ Build completed successfully!")
else:
    print("❌ Build failed. Check output above for errors.")
```

### Step 6: Check Results and Download
```python
import glob

print("🔍 Checking for APK files...")

# Look for APK files
apk_files = glob.glob("bin/*.apk")

if apk_files:
    print("🎉 APK files found:")
    for apk in apk_files:
        file_size = os.path.getsize(apk) / (1024 * 1024)  # Size in MB
        print(f"  📱 {apk} ({file_size:.1f} MB)")
    
    print("\n📁 To download your APK:")
    print("1. Click the folder icon on the left sidebar")
    print("2. Navigate to smart-word-practice-mobile/bin/")
    print("3. Right-click on the .apk file")
    print("4. Select 'Download'")
    
    print("\n🎯 Your APK is ready for installation on Android!")
    
else:
    print("❌ No APK files found.")
    print("💡 Try the alternative method:")
    print("   • Use GitHub Codespaces instead")
    print("   • Or check build logs for specific errors")

# List all files in bin directory for debugging
if os.path.exists('bin'):
    print("\n📋 Files in bin directory:")
    for file in os.listdir('bin'):
        print(f"  - {file}")
else:
    print("❌ bin directory not found")
```