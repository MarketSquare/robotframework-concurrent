from robotframework_concurrent import async_execution_keyword
import asyncio
from robot.api.deco import keyword


class eventDemo(async_execution_keyword.async_keyword_execution_base):
    def __init__(self):
        super().__init__()
    
    async def _task_async(self):
        await asyncio.sleep(1)
        self.run_keyword_async("Log", "Slept first 1s", "INFO")
        await asyncio.sleep(1)
        self.run_keyword_async("Log", "Slept second 1s", "INFO")

    @keyword
    async def  start_async_wait(self):
        self._task = asyncio.create_task(self._task_async())

    @keyword
    async def wait_for_events(self):
        await self._task
