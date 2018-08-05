import datetime
import time
from copy import copy
import random
import resource
import psutil
import collections

# Monitor construcs a Markdown formatted table showing time and
# memory usage within a monitored method.
# The call stack
#
# inc s | exc s | inc mem | exc mem | ncalls | call stack
# ----: | ----: | ------: | ------: | -----: | ----------
# 10000 |     1 |  12,000 |       1 |      1 | main()
#   0.1 |     1 |       1 |       1 |      1 | .Algorithm::setup()
# 10000 |  9000 |  12,000 |  11,850 |      1 | .Algorithm::train()
# 10000 |     1 |  12,000 |       1 |      1 | ..Datastream::fetch()

REPORT_HDR = "{:^12s} | {:^12s} | {:^12s} | {:^12s} | {:^8s} | {}"
REPORT_BRK = "{:->11s}: | {:->11s}: | {:->11s}: | {:->11s}: | {:->7s}: | :---"
REPORT_ROW = "{:>12g} | {:>12g} | {:>12g} | {:>12g} | {:>8d} | {}{}"


class Frame(object):
    def __init__(self, function_name):
        self.name = function_name
        self.time = 0.0
        self.ncalls = 0

        self.cpu = 0.0
        self.mem = 0.0

        # Contains anything directly called within the current frame
        self.calls = dict()

    def __hash__(self):
        return self.name.__hash__()

    def __copy__(self):
        # Copy doesn't copy the call data over to the new instance
        newone = type(self)(self.name)
        return newone

    def start(self, cpu, mem):
        self.ncalls += 1
        self.start_time = datetime.datetime.now()
        self.start_mem = mem
        self.start_cpu = cpu

    def stop(self, cpu, mem):
        self.time += (datetime.datetime.now() -
                      self.start_time).total_seconds()
        self.mem += mem - self.start_mem
        self.cpu += cpu - self.start_cpu

    def exclusive(self):
        exclusive = collections.namedtuple('exclusive', ['elp', 'cpu', 'mem'])

        exclusive.elp = self.time
        exclusive.cpu = self.cpu
        exclusive.mem = self.mem
        for _, i in self.calls.iteritems():
            exclusive.elp -= i.time
            exclusive.cpu -= i.cpu
            exclusive.mem -= i.mem

        return exclusive

    def report(self, indent=0):
        exc = self.exclusive()

        print REPORT_ROW.format(
                self.time,
                exc.elp,
                self.mem,
                exc.mem,
                self.ncalls,
                "." * indent,
                self.name)

        for _, i in self.calls.iteritems():
            i.report(indent + 1)


class Monitor(object):
    """
    Monitors long running parts of the system.
    """

    def __init__(self):
        self.call_stack = []
        self.process = psutil.Process()

        root_frame = Frame('__main__')
        self.call_stack.append(root_frame)
        with self.process.oneshot():
            root_frame.start(self.process.cpu_times().user,
                             self.process.memory_full_info().uss)

    def timed_method(self, function):
        """
        Decorator to measure the runtime of a function or method
        """
        # Decorate the function
        frame = Frame(function.__name__)

        def new_function(*args, **kwargs):
            self.push(frame)
            x = function(*args, **kwargs)
            self.pop()
            return x

        # This allows the frame name to be updated by the class decorator
        new_function.timing_frame = frame

        return new_function

    def timed_class(self, cls):
        # Finds all the timed methods and updates the frame name
        for m in dir(cls):
            member = getattr(cls, m)
            if callable(member):
                frame = getattr(member, 'timing_frame', 0)
                if frame != 0:
                    frame.name = cls.__name__ + "::" + frame.name

        return cls

    def push(self, frame):
        call_frame = self.call_stack[-1].calls.setdefault(frame, copy(frame))
        self.call_stack.append(call_frame)

        with self.process.oneshot():
            call_frame.start(self.process.cpu_times().user,
                             self.process.memory_full_info().uss)

    def pop(self):
        call_frame = self.call_stack.pop()
        
        with self.process.oneshot():
            call_frame.stop(self.process.cpu_times().user,
                            self.process.memory_full_info().uss)

    def report(self):

        print REPORT_HDR.format("ielp (s)",
                                "xelp (s)",
                                "imem (b)",
                                "xmem (b)",
                                "ncalls",
                                "call")
        print REPORT_BRK.format("", "", "", "", "")
        #self.call_stack[0].stop()
        self.call_stack[0].report()


# ===================================================================


monitor = Monitor()


@monitor.timed_class
class Foo:
    def __init__(self):
        self.memblock = []

    @monitor.timed_method
    def second(self, seconds):
        self.memblock += range(0, int(seconds * 10000))
        print len(self.memblock)
        time.sleep(seconds)
        pass

    @monitor.timed_method
    def buzz(self):
        for i in range(0, 5):
            r = random.random()
            print "Buzz: {}".format(r)
            self.second(r)

    @monitor.timed_method
    def fizz(self):
        for i in range(0, 5):
            r = random.random()
            print "Fizz: {}".format(r)
            self.second(r)


f = Foo()
f.fizz()
f.buzz()

monitor.report()
