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