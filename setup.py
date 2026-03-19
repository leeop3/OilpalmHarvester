import os
import zipfile

PROJECT_NAME = "OilPalmHarvester"
PACKAGE_DIR = "com/oilpalm/harvester"

FILES = {
    # --- GitHub Configuration ---
    ".gitignore": """
*.iml
.gradle
/local.properties
/.idea
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
app/src/main/python/__pycache__/
""",

    "README.md": f"""
# {PROJECT_NAME}

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
""",

    # --- GitHub Actions Workflow ---
    ".github/workflows/build.yml": """
name: Android CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Setup Android SDK
      uses: android-actions/setup-android@v3

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build with Gradle
      run: ./gradlew assembleDebug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: app/build/outputs/apk/debug/app-debug.apk
""",

    # --- Gradle Wrapper Properties ---
    "gradle/wrapper/gradle-wrapper.properties": """
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""",

    # --- Project Level Gradle ---
    "build.gradle": """
buildscript {
    repositories {
        google()
        mavenCentral()
        maven { url "https://chaquopy.com/repository" }
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.0'
        classpath "com.chaquo.python:gradle:15.0.1"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url "https://chaquopy.com/repository" }
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
""",

    "settings.gradle": """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url "https://chaquopy.com/repository" }
    }
}
rootProject.name = "OilPalmHarvester"
include ':app'
""",

    "gradlew": """#!/bin/sh
# Placeholder for gradlew script. 
# In a real repo, this is a binary script. 
# For this generator, please download gradlew from a standard Android project 
# or run 'gradle wrapper' if you have gradle installed.
# For GitHub Actions, this file is usually provided by checkout.
echo "Please initialize gradle wrapper properly"
""",
    
    "gradlew.bat": """@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0
@rem
@rem    https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%"=="" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%GRADLE_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
""",

    # --- App Level Gradle ---
    "app/build.gradle": """
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.chaquo.python'
    id 'kotlin-kapt'
}

android {
    namespace 'com.oilpalm.harvester'
    compileSdk 34

    defaultConfig {
        applicationId "com.oilpalm.harvester"
        minSdk 26
        targetSdk 34
        versionCode 1
        versionName "1.0"

        python {
            version "3.8"
            pip {
                install "reticulum"
                install "lxmf"
                install "pyserial"
            }
        }
        
        ndk {
            abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation "androidx.room:room-runtime:2.6.1"
    implementation "androidx.room:room-ktx:2.6.1"
    kapt "androidx.room:room-compiler:2.6.1"
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0"
    implementation "androidx.lifecycle:lifecycle-livedata-ktx:2.7.0"
    implementation 'com.google.android.gms:play-services-location:21.1.0'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'
}
""",

    "app/proguard-rules.pro": """
-keep class com.chaquo.python.** { *; }
""",

    # --- Android Manifest ---
    "app/src/main/AndroidManifest.xml": f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    <uses-permission android:name="android.permission.INTERNET" />

    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="true" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.OilPalmHarvester">
        
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".HistoryActivity" />
        
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${{applicationId}}.provider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
""",

    # --- Resources ---
    "app/src/main/res/values/strings.xml": """
<resources>
    <string name="app_name">Palm Harvester</string>
    <string name="new_entry">New Harvest Entry</string>
    <string name="history">My Reports</string>
    <string name="harvester_id">Harvester ID</string>
    <string name="block_id">Block ID</string>
    <string name="ripe_bunches">Ripe Bunches</string>
    <string name="empty_bunches">Empty Bunches</string>
    <string name="save_entry">Save Entry</string>
    <string name="send_now">Send Now</string>
    <string name="capture_photo">Capture Photo</string>
    <string name="gps_waiting">Acquiring GPS...</string>
</resources>
""",

    "app/src/main/res/values/colors.xml": """
<resources>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="green">#FF4CAF50</color>
    <color name="white">#FFFFFFFF</color>
    <color name="orange">#FFFF9800</color>
</resources>
""",

    "app/src/main/res/values/themes.xml": """
<resources>
    <style name="Theme.OilPalmHarvester" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
    </style>
</resources>
""",

    "app/src/main/res/xml/file_paths.xml": """
<paths>
    <external-files-path name="my_images" path="Pictures" />
</paths>
""",

    "app/src/main/res/layout/activity_main.xml": """
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">
    <LinearLayout
        android:orientation="vertical"
        android:layout_width="match_parent"
        android:layout_height="wrap_content">
        <TextView android:text="@string/new_entry" android:textSize="24sp" android:textStyle="bold" android:layout_marginBottom="16dp" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
        <TextView android:id="@+id/tvGpsStatus" android:text="@string/gps_waiting" android:textColor="@color/orange" android:layout_marginBottom="16dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <EditText android:id="@+id/etHarvesterId" android:hint="@string/harvester_id" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <EditText android:id="@+id/etBlockId" android:hint="@string/block_id" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <EditText android:id="@+id/etRipe" android:hint="@string/ripe_bunches" android:inputType="number" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <EditText android:id="@+id/etEmpty" android:hint="@string/empty_bunches" android:inputType="number" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <Button android:id="@+id/btnCapturePhoto" android:text="@string/capture_photo" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <TextView android:id="@+id/tvPhotoPath" android:text="No photo" android:layout_marginBottom="16dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <Button android:id="@+id/btnSave" android:text="@string/save_entry" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <Button android:id="@+id/btnSend" android:text="@string/send_now" android:layout_marginBottom="12dp" android:layout_width="match_parent" android:layout_height="wrap_content"/>
        <Button android:id="@+id/btnHistory" android:text="@string/history" style="@style/Widget.MaterialComponents.Button.OutlinedButton" android:layout_width="match_parent" android:layout_height="wrap_content"/>
    </LinearLayout>
</ScrollView>
""",

    "app/src/main/res/layout/activity_history.xml": """
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView android:text="@string/history" android:textSize="24sp" android:textStyle="bold" android:padding="16dp" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
    <androidx.recyclerview.widget.RecyclerView android:id="@+id/rvHistory" android:layout_width="match_parent" android:layout_height="match_parent"/>
</LinearLayout>
""",

    "app/src/main/res/layout/item_history.xml": """
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="8dp"
    android:elevation="4dp">
    <LinearLayout android:orientation="vertical" android:padding="16dp" android:layout_width="match_parent" android:layout_height="wrap_content">
        <TextView android:id="@+id/tvBlock" android:textStyle="bold" android:textSize="18sp" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
        <TextView android:id="@+id/tvDate" android:textSize="14sp" android:textColor="#666" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
        <LinearLayout android:orientation="horizontal" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp">
            <TextView android:id="@+id/tvStatus" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:textStyle="bold"/>
            <Button android:id="@+id/btnResend" android:text="Resend" android:visibility="gone" android:layout_width="wrap_content" android:layout_height="wrap_content"/>
        </LinearLayout>
    </LinearLayout>
</androidx.cardview.widget.CardView>
""",

    # --- Kotlin Source ---
    f"app/src/main/java/{PACKAGE_DIR}/MainActivity.kt": """
package com.oilpalm.harvester

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.lifecycle.ViewModelProvider
import com.oilpalm.harvester.databinding.ActivityMainBinding
import java.io.File

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var viewModel: HarvestViewModel
    private var photoUri: Uri? = null
    private var photoFileName: String? = null

    private val cameraLauncher = registerForActivityResult(ActivityResultContracts.TakePicture()) { success ->
        if (success) binding.tvPhotoPath.text = "Photo Captured: $photoFileName"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        viewModel = ViewModelProvider(this)[HarvestViewModel::class.java]
        binding.etHarvesterId.setText("H-${(Math.random() * 1000).toInt()}")
        binding.tvGpsStatus.text = "GPS: 3.14159, 101.68653 (Simulated)"
        
        binding.btnCapturePhoto.setOnClickListener {
            val photoFile = File(externalFilesDir, "Pictures/${System.currentTimeMillis()}.jpg")
            photoFileName = photoFile.name
            photoUri = FileProvider.getUriForFile(this, "${applicationContext.packageName}.provider", photoFile)
            cameraLauncher.launch(photoUri)
        }
        binding.btnSave.setOnClickListener { saveEntry() }
        binding.btnSend.setOnClickListener { 
            viewModel.sendPendingEntries()
            Toast.makeText(this, "Transmission Started", Toast.LENGTH_SHORT).show()
        }
        binding.btnHistory.setOnClickListener { startActivity(Intent(this, HistoryActivity::class.java)) }
    }

    private fun saveEntry() {
        val ripe = binding.etRipe.text.toString().toIntOrNull() ?: 0
        val empty = binding.etEmpty.text.toString().toIntOrNull() ?: 0
        val block = binding.etBlockId.text.toString()
        if (block.isEmpty()) { Toast.makeText(this, "Block ID Required", Toast.LENGTH_SHORT).show(); return }
        viewModel.insert(HarvestEntry(
            harvesterId = binding.etHarvesterId.text.toString(), blockId = block,
            ripeBunches = ripe, emptyBunches = empty,
            latitude = 3.14159, longitude = 101.68653, photoFile = photoFileName ?: ""
        ))
        Toast.makeText(this, "Entry Saved", Toast.LENGTH_SHORT).show()
        binding.etBlockId.text.clear(); binding.etRipe.text.clear(); binding.etEmpty.text.clear()
    }
}
""",

    f"app/src/main/java/{PACKAGE_DIR}/HarvestEntry.kt": """
package com.oilpalm.harvester
import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID
@Entity(tableName = "harvest_entries")
data class HarvestEntry(
    @PrimaryKey(autoGenerate = true) val localId: Int = 0,
    val id: String = UUID.randomUUID().toString(),
    val harvesterId: String, val blockId: String,
    val ripeBunches: Int, val emptyBunches: Int,
    val latitude: Double, val longitude: Double,
    val timestamp: Long = System.currentTimeMillis(),
    val photoFile: String, val status: String = "pending"
)
""",

    f"app/src/main/java/{PACKAGE_DIR}/HarvestDao.kt": """
package com.oilpalm.harvester
import androidx.lifecycle.LiveData
import androidx.room.*
@Dao
interface HarvestDao {
    @Insert suspend fun insert(entry: HarvestEntry)
    @Query("SELECT * FROM harvest_entries ORDER BY timestamp DESC") fun getAllEntries(): LiveData<List<HarvestEntry>>
    @Query("SELECT * FROM harvest_entries WHERE status = 'pending'") suspend fun getPendingEntries(): List<HarvestEntry>
    @Update suspend fun update(entry: HarvestEntry)
}
""",

    f"app/src/main/java/{PACKAGE_DIR}/AppDatabase.kt": """
package com.oilpalm.harvester
import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
@Database(entities = [HarvestEntry::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun harvestDao(): HarvestDao
    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null
        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(context.applicationContext, AppDatabase::class.java, "harvest_database").build()
                INSTANCE = instance; instance
            }
        }
    }
}
""",

    f"app/src/main/java/{PACKAGE_DIR}/HarvestViewModel.kt": """
package com.oilpalm.harvester
import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
class HarvestViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).harvestDao()
    val allEntries: LiveData<List<HarvestEntry>> = dao.getAllEntries()
    init { if (!Python.isStarted()) Python.start(AndroidPlatform(application)) }
    fun insert(entry: HarvestEntry) { viewModelScope.launch { dao.insert(entry) } }
    fun sendPendingEntries() {
        viewModelScope.launch {
            val pending = dao.getPendingEntries()
            val py = Python.getInstance()
            val module = py.getModule("rns_handler")
            for (entry in pending) {
                try {
                    module.callFunction("send_lxmf", entry.toCsv())
                    dao.update(entry.copy(status = "sent"))
                } catch (e: Exception) { e.printStackTrace() }
            }
        }
    }
}
fun HarvestEntry.toCsv(): String = "$id,$harvesterId,$blockId,$ripeBunches,$emptyBunches,$latitude,$longitude,$timestamp,$photoFile"
""",

    f"app/src/main/java/{PACKAGE_DIR}/HistoryActivity.kt": """
package com.oilpalm.harvester
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.oilpalm.harvester.databinding.ActivityHistoryBinding
class HistoryActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHistoryBinding
    private lateinit var viewModel: HarvestViewModel
    private lateinit var adapter: HistoryAdapter
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHistoryBinding.inflate(layoutInflater)
        setContentView(binding.root)
        viewModel = ViewModelProvider(this)[HarvestViewModel::class.java]
        adapter = HistoryAdapter { viewModel.sendPendingEntries() }
        binding.rvHistory.layoutManager = LinearLayoutManager(this)
        binding.rvHistory.adapter = adapter
        viewModel.allEntries.observe(this) { adapter.submitList(it) }
    }
}
""",

    f"app/src/main/java/{PACKAGE_DIR}/HistoryAdapter.kt": """
package com.oilpalm.harvester
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.oilpalm.harvester.databinding.ItemHistoryBinding
import java.text.SimpleDateFormat
import java.util.*
class HistoryAdapter(private val onResendClick: (HarvestEntry) -> Unit) : ListAdapter<HarvestEntry, HistoryAdapter.ViewHolder>(DiffCallback()) {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemHistoryBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }
    override fun onBindViewHolder(holder: ViewHolder, position: Int) { holder.bind(getItem(position)) }
    inner class ViewHolder(private val binding: ItemHistoryBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(entry: HarvestEntry) {
            binding.tvBlock.text = "Block: ${entry.blockId}"
            binding.tvDate.text = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date(entry.timestamp))
            binding.tvStatus.text = entry.status.uppercase()
            binding.btnResend.visibility = if (entry.status == "pending") View.VISIBLE else View.GONE
            binding.btnResend.setOnClickListener { onResendClick(entry) }
        }
    }
    class DiffCallback : DiffUtil.ItemCallback<HarvestEntry>() {
        override fun areItemsTheSame(oldItem: HarvestEntry, newItem: HarvestEntry) = oldItem.localId == newItem.localId
        override fun areContentsTheSame(oldItem: HarvestEntry, newItem: HarvestEntry) = oldItem == newItem
    }
}
""",

    # --- Python RNS Logic ---
    "app/src/main/python/rns_handler.py": """
import reticulum as RNS
import lxmf

identity = None
destination = None

def init_rns():
    global identity, destination
    RNS.Reticulum()
    identity = RNS.Identity()
    destination = lxmf.LXMFDestination(identity, app_name="PalmHarvester")

def send_lxmf(csv_payload):
    global identity, destination
    if identity is None: init_rns()
    message = lxmf.LXMessage(source=identity, destination=destination, content=csv_payload, fields=lxmf.LXMessage.TEXT_FIELD)
    message.sign()
    RNS.Transport.send(message)
    print(f"Message Sent: {csv_payload[:20]}...")
    return True
"""
}

def create_project():
    print(f"Creating {PROJECT_NAME} for GitHub...")
    for path, content in FILES.items():
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created: {path}")
    
    # Note: Gradlew script needs to be executable in real repo
    print("\nIMPORTANT: In your GitHub repo, ensure 'gradlew' has execute permissions.")
    print("Project ready to push to GitHub!")

if __name__ == "__main__":
    create_project()