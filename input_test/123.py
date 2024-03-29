import asyncio


async def main():
    n = 8
    for i in range(1, n+1):
        await asyncio.sleep(1)
        print(i)

        if i == 3:
            asyncio.ensure_future(run_subprocess())


async def run_subprocess():
    print('Starting subprocess')
    code = 'import time, datetime; time.sleep(3); print(datetime.datetime.now())'
    proc = await asyncio.create_subprocess_exec(
        'python', '-c', code, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    output = stdout.strip().decode('utf-8')
    print('Subprocess output: ' + output)
    print('Subprocess finished with return code {}'.format(proc.returncode))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()   