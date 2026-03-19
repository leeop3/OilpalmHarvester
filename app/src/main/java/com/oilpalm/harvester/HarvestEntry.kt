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