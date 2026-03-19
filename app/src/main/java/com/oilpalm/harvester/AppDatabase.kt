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