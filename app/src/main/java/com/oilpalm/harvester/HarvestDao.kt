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