import sched
import threading
from threading import Timer
import time
import datetime as dt
from datetime import datetime, timedelta
import functools


def fn(*args, **kwargs):
    print(" - ", time.ctime())
class Scheduler(threading.Thread):
    def __init__(self, start: bool = True):
        self._scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
        self._running = True
        super().__init__(daemon=False)
        if start:
            self.start()

    def run_at(self, time, action, args=None, kwargs=None):
        self._scheduler.enterabs(
            time=time,
            priority=0,
            action=action,
            argument=args or tuple(),
            kwargs=kwargs or dict())

    def run(self):
        while self._running:
            delta = self._scheduler.run(blocking=False) or 0.5
            self._scheduler.delayfunc(min(delta, 0.5))

    def run_every(self, seconds, fn, *args, **kwargs):
        def _run_after(seconds, function, *args, **kwargs):
            self._scheduler.enter(
                delay=seconds,
                priority=0,
                action=function,
                argument=args,
                kwargs=kwargs,
            )

        @functools.wraps(fn)
        def _function(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            finally:
                _run_after(seconds, _function, args=args, kwargs=kwargs)

        _run_after(seconds, _function, args=args, kwargs=kwargs)

    def run_scheduled(self, date: dt.datetime, delta: dt.timedelta, action: callable, args=None, kwargs=None):
        def first_launch():
            self.run_every(
                seconds=delta.total_seconds(),                
                fn=action,
                argument=args,
                kwargs=kwargs,
            )

        date_timestamp = date.timestamp()
        timestamp_delta = date_timestamp 
        self.run_at(time=timestamp_delta, action=first_launch, args=args, kwargs=kwargs)

    def stop(self):
        self._running = False

fn()
d = dt.datetime.now().replace(second=25)
x = Scheduler()
x.run_scheduled(date=d, delta=dt.timedelta(seconds=3), action=fn, args=())

