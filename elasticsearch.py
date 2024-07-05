
#rawdata: rawdata_per_day; 
    #ret_lc: least count of retention;
    #ncop: no.of backups or ES_replica
    #all data expressions r in GB
    #considering ram of nodes as per availability 
    #dict_ram an dictionary of various avaiable rams 
    #scale_factor - traffic increase 
    #mem_dat_node - as per the 
    #tot_ind - no.of idices to be created 
    #indep_tasks - no.of independent tasks per moment
from math import ceil
from typing import ClassVar
from pydantic import BaseModel
from typing import Literal

class EstimatorResult(BaseModel):
    cpu_cores: int
    ram_per_node: int
    memory_gb: int
    node_count: int
    data_node: int
    master_node: int
    price_model_name: Literal["basic", "standard", "premium"]
    memory_node: int

class ESClusterEstimator:

    def __init__(self, rawdata, scale_factor, indep_tasks, tot_tasks, node_class = None, mem_data_ratio=0):
        self.rawdata = rawdata        
        self.scale_factor = scale_factor
        self.node_class = node_class
        self.mem_data_ratio = mem_data_ratio
        self.indep_tasks = indep_tasks
        self.tot_tasks = tot_tasks
    
    def total_storage_requirement(self, ret_lc, ncop, indexing_comp_ratio, lake_ratio):
        tot_data = self.rawdata * ret_lc * (ncop + 1)
        disk_tot_data = tot_data*(1+0.3)*(indexing_comp_ratio)*lake_ratio
        return tot_data, disk_tot_data
    
    def mapping_scenario(self, disk_tot_data):
        tot_data, disk_tot_data = total_storage_requirement(self, ret_lc, ncop, indexing_comp_ratio, lake_ratio)
        if disk_tot_data <= 4000:
            data_node = 2 + ceil((disk_tot_data - 2000)/1000)
            master_node = 1
            ram = 16
            tot_node = data_node + master_node
            capacity_shard = 20
            return Basic_es(self, tot_node, data_node, ram, capacity_shard, disk_tot_data)
        if disk_tot_data > 4000 & disk_tot_data <= 8000:
            data_node = 2 + ceil((disk_tot_data - 4000)/1000)
            master_node = 1
            ram = 32
            tot_node = data_node + master_node
            capacity_shard = 30
            return Standard_es(self, tot_node, data_node, ram, capacity_shard, disk_tot_data)
        
        else:
            ram = 64
            capacity_shard = 40
            return Premium_es(self, ram, capacity_shard, disk_tot_data, tot_data)

    def Basic_es(self, tot_node, data_node, ram, capacity_shard, disk_tot_data):
        disk_data = disk_tot_data/data_node
        mem_dat_ratio = self.memory_data_ratio()
        memory_node = ram/mem_dat_ratio
        n_cores = 4
        Tot_cores = n_cores*tot_node
        tot_ram = ram*n_node
        tot_shards = self.shard_chars(capacity_shard, memory_node)
        return EstimatorResult(
            cpu_cores=Tot_cores,
            ram_per_node=ram,
            memory_gb=disk_tot_data,
            node_count=tot_node,
            data_node=data_node,
            master_node=tot_node - data_node,
            price_model_name="basic",
            memory_node=disk_data
        )
    
    def Standard_es(self, tot_node, data_node, ram, capacity_shard, disk_tot_data):
        disk_data = disk_tot_data/data_node
        mem_dat_ratio = self.memory_data_ratio()
        memory_node = ram/mem_dat_ratio
        n_cores = 8
        Tot_cores = n_cores*tot_node
        tot_ram = ram*n_node
        tot_shards = self.shard_chars(capacity_shard, memory_node)
        return EstimatorResult(
            cpu_cores=Tot_cores,
            ram_per_node=ram,
            memory_gb=disk_tot_data,
            node_count=tot_node,
            data_node=data_node,
            master_node=tot_node - data_node,
            price_model_name="standard",
            memory_node=disk_data
        )
        
    def Premium_es(self, ram, capacity_shard, disk_tot_data, tot_data):
        mem_dat_ratio = self.memory_data_ratio()
        n_node, disk_data, memory_node = self.node_chars(tot_data, ram, disk_tot_data)
        tot_shards = self.shard_chars(capacity_shard, memory_node)
        n_cores = max(16, 2*n_node)
        Tot_cores = n_cores*n_node
        tot_ram = ram*n_node
        return EstimatorResult(
            cpu_cores=Tot_cores,
            ram_per_node=ram,
            memory_gb=disk_tot_data,
            node_count=tot_node,
            data_node=data_node,
            master_node=tot_node - data_node,
            price_model_name="premium",
            memory_node=disk_data
        )
    def memory_data_ratio(self):
        if self.mem_dat_ratio != 0:
            return mem_dat_ratio
        if self.node_class == 'warm+hot':  # hybrid nodes few hot + few warm - better optimisation
            self.mem_dat_ratio = 160
        elif self.node_class == 'warm':
            self.mem_dat_ratio = 100
        else:
            self.mem_dat_ratio = 30 
        return self.mem_dat_ratio

    def node_chars(self, tot_data, ram, disk_tot_data):
        data_node = 1 + round(tot_data / ram / mem_dat_ratio)
        memory_node = ram/mem_dat_ratio
        if(n_node < 10):
            master_node = 1
        else: master_node = 3
        n_node = data_node + master_node
        disk_data = disk_tot_data/ data_node
        return data_node, master_node, disk_data, memory_node 

    def shard_chars(self, capacity_shard, memory_node):
        #indep_tasks, tasks are per an instant
        n_shards = (memory_node / capacity_shard) * (1 + self.indep_tasks/self.tot_tasks)*(1 + self.scale_factor)
        n_replica = n_shards
        tot_shards = 2*n_shards
        return tot_shards

# capacity_shard is to be obtained experimentally depending upon data_var, dead_time
#dead_time - considering single shard depends on latency, storage type