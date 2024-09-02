class Metrics:
    def __init__(self, metricName, namespace):
        self.metricName = metricName
        self.namespace = namespace
    
    def getMetricName(self):
        return self.metricName
    
    def getNamespace(self):
        return self.namespace


ECS_SERVER = [Metrics("CPUUtilization", "acs_ecs_dashboard"), 
             Metrics("memory_usedutilization", "acs_ecs_dashboard"), 
             Metrics("DiskReadIOPS", "acs_ecs_dashboard"), 
             Metrics("DiskWriteIOPS", "acs_ecs_dashboard")
            ]

RDS_MYSQL = [Metrics("CpuUsage", "acs_rds_dashboard"), 
             Metrics("MemoryUsage", "acs_rds_dashboard"), 
             Metrics("IOPSUsage", "acs_rds_dashboard"), 
             Metrics("DiskUsage", "acs_rds_dashboard")
            ]

RDS_PosgreSQL = [Metrics("cpu_usage", "acs_rds_dashboard"), 
             Metrics("mem_usage", "acs_rds_dashboard"), 
             Metrics("iops_usage", "acs_rds_dashboard"), 
             Metrics("local_fs_size_usage", "acs_rds_dashboard")
            ]

RDS_SQLServer = [Metrics("SQLServer_CpuUsage", "acs_rds_dashboard"), 
             Metrics("mem_usage", "acs_rds_dashboard"), 
             Metrics("SQLServer_IOPS", "acs_rds_dashboard"), 
             Metrics("SQLServer_DiskUsage", "acs_rds_dashboard")
            ]

REDIS_STANDARD = [Metrics("StandardCpuUsage", "acs_kvstore"), 
             Metrics("StandardMemoryUsage", "acs_kvstore"), 
             Metrics("StandardUsedConnection", "acs_kvstore"), 
             Metrics("StandardUsedQPS", "acs_kvstore")
        ]