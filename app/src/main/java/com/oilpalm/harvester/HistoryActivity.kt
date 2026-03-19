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