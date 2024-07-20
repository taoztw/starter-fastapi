result_expires = 60 * 40  # 任务过期时间,celery任务执行结果的超时时间

# 规定完成任务的时间
task_time_limit = (
    36000  # 在2000s内完成任务，否则执行该任务的worker将被杀死，任务移交给父进程
)
broker_transport_options = {"visibility_timeout": 1800}

worker_max_tasks_per_child = 40  # 每个worker执行了多少任务就会死掉，默认是无限的

# 防止死锁
celeryd_force_execv = True
task_reject_on_worker_lost = True

# 预取任务数
worker_prefetch_multiplier = 1
