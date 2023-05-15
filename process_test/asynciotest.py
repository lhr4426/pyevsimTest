import asyncio
import subprocess as sp
import multiprocessing as mp
import schedule
import time
import psutil

async def get_result(proc) :
    out, err = proc.communicate()
    print(out)

async def find_state(proc) :
    pid = proc.pid
    print(psutil.Process(pid).status())

async def main() :
    proc = sp.Popen(['dotnet', 'run'], stdout=sp.PIPE, stderr=sp.PIPE)
    print(proc.pid)
    as1 = get_result(proc)
    as2 = find_state(proc)
    await asyncio.gather(as1, as2)

my_loop = asyncio.get_event_loop()
my_loop.run_until_complete(main())
my_loop.close()

