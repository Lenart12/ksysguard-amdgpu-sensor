# ksysguard-amdgpu-sensor
Sensor module for KSysGuard for AMD graphics cards

---
This sensor module parses data from [radeontop](https://github.com/clbr/radeontop) and sends it to KSysGuard over its protocol.

With it you can monitor the following values:

| Short 	| Display name                	|
|:-----:	|-----------------------------	|
|  gpu  	| Graphics pipe               	|
|   ee  	| Event engine                	|
|  vgt  	| Vertex Grouper + Tesselator 	|
|   ta  	| Texture Addresser           	|
|   sx  	| Shader Export               	|
|   sh  	| Sequencer Instruction Cache 	|
|  spi  	| Shader Interpolator         	|
|   sc  	| Scan Converter              	|
|   pa  	| Primitive Assembly          	|
|   db  	| Depth Block                 	|
|   cb  	| Color Block                 	|
|  vram 	| Video ram                   	|
|  gtt  	| Graphics translation table  	|
|  mclk 	| Memory clock                	|
|  sclk 	| Shader clock                	|

---
### Requirements
1. [radeontop](https://github.com/clbr/radeontop)
2. [aioconsole](https://github.com/vxgmichel/aioconsole)

---
### Instalation
To install this open KSysGuard and click File -> Sensor remote machine...
There give the name to the host (eg. AMDGPU)
Select costum command and in the command box
give the full path to this file (eg. /home/hunter2/ksysguard-amdgpu-sensor/amdgpu-sensor.py)

NOTE: Becouse of how radeontop works it requires sudo;
this program assumes radeontop will be run as sudo without
any password so if it doesn't you have to fix that
(eg. `sudo chown root:root /usr/bin/radeontopsudo chmod a+s /usr/bin/radeontop`)

![Preview](https://i.imgur.com/QPB63Sg.png)

Made and tested in python 3.7.3
