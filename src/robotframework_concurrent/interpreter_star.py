import time
import robot.api.logger as logger
from pathlib import Path
import itertools
from typing import Any, Union
try:
    import interpreters
except ImportError:
    from interpreters_backport import interpreters


class interpreter_star():
    _start_cnt = itertools.count()
    _address = None

    def __init__(self, target_suite: Union[None, Path, str]=None):
        self._target_suite = target_suite        
        self._interpreter = None

    def Start_interpreter(self) -> None:
        if self._target_suite:
            logger.error(self._target_suite)
            self.out_dir = f"{self._target_suite}_{next(self._start_cnt)}_output"
            self._inQ = interpreters.create_queue()
            self._outQ = interpreters.create_queue()
            self._interpreter = interpreters.create()

            def _start_robotframework_in_subinterpreter():
                import __main__
                import robot
                import robotframework_concurrent.interpreter_star
                import pathlib
                try:
                    import interpreters
                except ImportError:
                    from interpreters_backport import interpreters
                
                outdir = pathlib.Path(getattr(__main__, "__out_dir"))
                outdir.mkdir(parents=True, exist_ok=True)

                with open(outdir / "output.log", "w", buffering=1) as stdout:
                    robotframework_concurrent.interpreter_star.interpreter_star._inQ = interpreters.Queue(getattr(__main__, "__outQ"))
                    robotframework_concurrent.interpreter_star.interpreter_star._outQ = interpreters.Queue(getattr(__main__, "__inQ"))
                    robot.run(getattr(__main__, "__target_suite"), outputdir=getattr(__main__, "__out_dir"), stdout=stdout, stderr=stdout)

            self._interpreter.prepare_main(__outQ=self._outQ.id, __inQ=self._inQ.id, __out_dir=self.out_dir, __target_suite=self._target_suite)
            self._subinterpreter_thread = self._interpreter.call_in_thread(_start_robotframework_in_subinterpreter)


    def send_message(self, message: Any) -> None:
        self._outQ.put(message)

    def recv_message(self) -> Any:
        return self._inQ.get()
    
    def interpreter_Should_Have_Terminated(self, timeout:int =1) -> None:
        assert self._interpreter is not None, "Process was not started"
        deadline = time.time() + timeout
        while self._interpreter.is_running() and time.time() < deadline:
            time.sleep(0.1)
        assert not self._interpreter.is_running(), f"Process {self._target_suite} has not terminated within {timeout} seconds"

    def interpreter_Should_Be_Running(self) -> None:
        assert self._sp is not None, "Process was not started"
        if not self._interpreter.is_running():
            raise Exception(f"Process {self._target_suite} has terminated prematurely (output: {self._out_dir})")
    