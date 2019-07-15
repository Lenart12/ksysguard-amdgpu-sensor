#!/usr/bin/env python

from contextlib import suppress
import aioconsole
import asyncio
import re

class Sensor:
    def __init__(self, name, minval, maxval, unit, valtype='float'):
        self.name = name            # Display name
        self.minval = minval        # The smallest the value will ever be
        self.maxval = maxval        # The largest the value will ever be
        self.unit = unit            # Units of the value
        self.valtype = valtype      # Type of the value

    def info(self):
        inf = f'{self.name}\t{self.minval}\t{self.maxval}'
        if self.unit:
            inf += f'\t{self.unit}'
        return inf

def createSensors():
    sensors = {
    # 'bus'	:	Sensor('BUS', 0, 0, '', 'integer'),
    'gpu'	:	Sensor('Graphics pipe', 0, 100, '%'),
    'ee'	:	Sensor('Event engine', 0, 100, '%'),
    'vgt'	:	Sensor('Vertex Grouper + Tesselator', 0, 100, '%'),
    'ta'	:	Sensor('Texture Addresser', 0, 100, '%'),
    'sx'	:	Sensor('Shader Export', 0, 100, '%'),
    'sh'	:	Sensor('Sequencer Instruction Cache', 0, 100, '%'),
    'spi'	:	Sensor('Shader Interpolator', 0, 100, '%'),
    'sc'	:	Sensor('Scan Converter', 0, 100, '%'),
    'pa'	:	Sensor('Primitive Assembly', 0, 100, '%'),
    'db'	:	Sensor('Depth Block', 0, 100, '%'),
    'cb'	:	Sensor('Color Block', 0, 100, '%'),
    'vram'	:	Sensor('Video ram', 0, 100, '%'),
    'gtt'	:	Sensor('Graphics translation table', 0, 100, '%'),
    'mclk'	:	Sensor('Memory clock', 0, 100, '%'),
    'sclk'	:	Sensor('Shader clock', 0, 100, '%')
    }
    return sensors

def monitors(sensors):
    monitors = ''
    for key, sensor in sensors.items():
        monitors += key + '\t' + sensor.valtype + '\n'
    
    return monitors[:-1]

class RadeonMonitor:
    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            'radeontop', '-d', '-',
            stdout=asyncio.subprocess.PIPE
        )
        await asyncio.sleep(1)
        self.task = asyncio.create_task(self.updateLine())
        self.lastline = ''

    async def stop(self):
        try:
            self.task.cancel()
        except asyncio.CancelledError:
            pass
        self.process.kill()

    async def updateLine(self):
        async for line in self.process.stdout:
            self.lastline = line.decode('utf-8')

    def extractValue(self, valueKey):
        m = re.search(r'(?:{} )(\d+?\.\d+?)(?:%)'.format(valueKey), self.lastline)

        if m:
            return m.group(1)
        else:
            return None

async def main():
    monitor = RadeonMonitor()
    await monitor.start()

    sensors = createSensors()

    await aioconsole.aprint('ksysguardd 1.2.0')
    while True:
        cmd = await aioconsole.ainput('ksysguardd> ')

        if cmd == 'monitors':
            await aioconsole.aprint(monitors(sensors))
        elif cmd == 'lastline':
            await aioconsole.aprint(monitor.lastline)
        elif cmd == 'quit':
            await monitor.stop()
            return
        else:
            if cmd.endswith('?'):
                try:
                    await aioconsole.aprint( sensors[cmd[:-1]].info() )
                except KeyError:
                    pass
            else:
                val = monitor.extractValue(cmd)
                if val:
                    await aioconsole.aprint(val)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        for task in asyncio.Task.all_tasks():
            task.cancel()
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        loop.close()

