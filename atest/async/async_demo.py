import asyncio
from robot.api.deco import keyword
from robotframework_concurrent.concurrent_keyword import concurrent_keyword_execution_base


class async_demo(concurrent_keyword_execution_base):
    def __init__(self):
        super().__init__()
    
    async def _task_async(self):
        await asyncio.sleep(1)
        self.run_keyword_concurrent("Log", "Slept first 1s", "INFO")
        await asyncio.sleep(2)
        self.run_keyword_concurrent("Log", "Slept second 2s", "INFO")

    @keyword
    async def  start_async_wait(self):
        self._task = asyncio.create_task(self._task_async())

    @keyword
    async def wait_for_events(self):
        await self._task
