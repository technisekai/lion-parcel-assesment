from pipe_task import pipeline_task
from pipe_bonus import pipeline_bonus
from dagster import (
    Definitions, 
    ScheduleDefinition
)

TIMEZONE_NAME = "Asia/Jakarta"

job_task = pipeline_task.to_job()
job_task_schedule = ScheduleDefinition(
    job=job_task, cron_schedule="0 */1 * * *", execution_timezone=TIMEZONE_NAME
)

job_bonus = pipeline_bonus.to_job()
job_bonus_schedule = ScheduleDefinition(
    job=job_bonus, cron_schedule="0 0 1 */1 *", execution_timezone=TIMEZONE_NAME
)

defs = Definitions(
    jobs=[job_task, job_bonus],
    schedules=[job_task_schedule, job_bonus_schedule],
)