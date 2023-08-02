from asyncio import sleep
from datetime import datetime
from datetime import timedelta

from asyncpg import Pool
from taskiq import Context, TaskiqDepends

from src.infrastructure.database.db.data import DataDB
from src.infrastructure.worker.broker import broker
from src.infrastructure.worker.utils import select_task



@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def send_messages(context: Context = TaskiqDepends()) -> None:
    pool: Pool = context.state.pool
    data_db: DataDB = context.state.data_db
    
    async with pool.acquire() as connect:
        result = await data_db.get_data(connect)
    
    if result is None:
        return
    for data in result:
        
        func = select_task.select(int(data.stage))
        
        if func is None:
            continue
        
        task = await func.kiq(tid=data.tid, cid=data.cid)
        task_result = await task.wait_result(timeout=3)
        
        if task_result.is_err:
            async with pool.acquire() as connect:
                await data_db.update_data(
                    connect,
                    tid=data.tid,
                    stage=data.stage,
                    datetime=datetime.now().replace(
                    microsecond=0, second=0
                    ) + timedelta(minutes=1)
                )
        await sleep(0.1)
