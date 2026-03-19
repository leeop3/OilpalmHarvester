# OilPalmHarvester

Android application for oil palm harvesters to record and transmit harvest data using RNS/LXMF over Bluetooth.

## Features
- Offline data entry
- GPS & Photo capture
- RNS/LXMF Transmission via Bluetooth (RNode)
- Local SQLite Storage

## Build Instructions (Without Android Studio)

### Option 1: GitHub Actions (Recommended)
1. Push this code to your GitHub repository.
2. Go to the **Actions** tab.
3. The build will start automatically.
4. Download the APK from the **Artifacts** section.

### Option 2: Local Command Line
Requires: JDK 17+, Android SDK (cmdline-tools)
1. Set `ANDROID_HOME` environment variable.
2. Create `local.properties` with `sdk.dir=/path/to/sdk`.
3. Run: `./gradlew assembleDebug`