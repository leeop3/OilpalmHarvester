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