#!/usr/bin/env python3
"""Send local test commands to a runner started with --automation-dir build/control."""
import argparse
from pathlib import Path
import time
import uuid

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('command',choices=['status','step','pad','clear_pad','screenshot','pause','resume','stop','save_state','load_state'])
parser.add_argument('values',nargs='*',help='For pad: a=1 start=1 main_x=0.5; for screenshot: filename.png')
parser.add_argument('--frames',type=int,default=3)
parser.add_argument('--capture',help='For step: new PNG filename captured before pausing')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'build/control'
if args.command=='status':
    print((root/'status.txt').read_text());raise SystemExit()
if not (root/'status.txt').exists() or time.time()-(root/'status.txt').stat().st_mtime>5:
    raise SystemExit('No recent runtime status; start the runner with --automation-dir build/control')
lines=[f'command={"pad_frames" if args.command in ("pad", "step") else args.command}']
if args.command in ('pad','step'):
    if not 1<=args.frames<=36000:parser.error('frames must be 1..36000')
    lines.extend(['port=0',f'frames={args.frames}'])
    buttons={'a','b','x','y','z','start','l','r','l_analog','r_analog','dpad_up','dpad_down','dpad_left','dpad_right'}
    axes={'main_x','main_y','c_x','c_y'}
    for value in args.values:
        key,separator,number=value.partition('=')
        if separator!='=' or key not in buttons|axes:parser.error('unknown pad field')
        try:amount=float(number)
        except ValueError:parser.error('pad values must be numeric')
        if not (-1 if key in axes else 0)<=amount<=1:parser.error('pad value outside range')
        lines.append(f'{key}={amount}')
elif args.command in ('screenshot', 'save_state', 'load_state'):
    extension = '.png' if args.command == 'screenshot' else '.sav'
    if len(args.values)!=1 or Path(args.values[0]).name!=args.values[0] or not args.values[0].endswith(extension):
        parser.error('provide one plain filename ending in '+extension)
    lines.append('path=artifacts/'+args.values[0])
elif args.values:parser.error('this command takes no values')
commands=root/'commands';commands.mkdir(parents=True,exist_ok=True)
if args.command == 'step':
    if args.frames > 600:
        parser.error('step is limited to 600 frames')
    if not args.capture or Path(args.capture).name != args.capture or not args.capture.endswith('.png'):
        parser.error('step requires --capture with one plain PNG filename')
    capture=root/'artifacts'/args.capture
    if capture.exists():
        parser.error('capture already exists; use a new filename')
    if any(commands.glob('*.txt')):
        raise SystemExit('Pending commands exist; wait for them before a step')
    sequence=[['command=resume'],lines,
              ['command=screenshot','path=artifacts/'+args.capture],
              ['command=pad_frames','port=0','frames=3'],['command=pause']]
else:
    if args.capture:
        parser.error('--capture is only valid with step')
    sequence=[lines]
base=time.time_ns()
names=[]
for index, command_lines in enumerate(sequence):
    name=f'{base+index}-{uuid.uuid4().hex}.txt'
    temp=root/(name+'.tmp');temp.write_text('\n'.join(command_lines)+'\n');temp.rename(commands/name)
    names.append(name)
if args.command != 'step':
    print('Queued:',names[0])
else:
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        failed=[name for name in names if (root/'failed'/name).exists()]
        if failed:
            raise SystemExit('Runtime rejected step command: '+', '.join(failed))
        status=(root/'status.txt').read_text()
        if (root/'processed'/names[-1]).exists() and capture.exists() and 'state=paused\n' in status:
            print('Paused; capture:',capture)
            break
        time.sleep(0.1)
    else:
        raise SystemExit('Step timed out; inspect runtime status and command queue before retrying')
