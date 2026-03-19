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