#!/usr/bin/env python3
"""Bounded native-module smoke test. This does not certify visual/gameplay fidelity.
Source tools/local-env.sh first when using the local Ubuntu SDK.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
from prepare_user import prepare_user

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--seconds',type=int,default=30)
parser.add_argument('--headless',action='store_true')
parser.add_argument('--graphics',default='OGL')
args=parser.parse_args()
if not 1 <= args.seconds <= 600:
    parser.error('--seconds must be between 1 and 600')
root=Path(__file__).resolve().parents[1]
operation_lock=(root/'build/.operation.lock').open('a')
try:
    fcntl.flock(operation_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:
    raise SystemExit('Another project operation is running; refusing concurrent execution')
lock=json.loads((root/'config/sources.lock.json').read_text())
if hashlib.sha256((root/'extracted/G2VP08/sys/main.dol').read_bytes()).hexdigest()!=lock['dol_sha256']:
    raise SystemExit('Unexpected main.dol')
module=Path((root/'build/modules/G2VP08/active-module.txt').read_text().strip())
if not module.is_file():
    raise SystemExit('Active native module does not exist')
prepare_user(root)
logs=root/'build/logs';logs.mkdir(parents=True,exist_ok=True)
stamp=time.strftime('%Y%m%d-%H%M%S')+f'-{os.getpid()}'
control=logs/f'smoke-{stamp}-control'
control.mkdir()
log=logs/f'smoke-{stamp}.log'
command=[str(root/'build/moderngekko/moderngekko-run'),'--game',str(root/'extracted/G2VP08'),'--module',str(module),'--user-dir',str(root/'build/user'),'--no-mods','--automation-dir',str(control)]
command += ['--headless'] if args.headless else ['-X11','--graphics',args.graphics]
env=dict(os.environ,XDG_CACHE_HOME=str(root/'build/cache'),STATICRECOMP_DISPATCH_SAMPLES='1')
forced=False
with log.open('w') as output:
    process=subprocess.Popen(command,stdout=output,stderr=subprocess.STDOUT,env=env,cwd=root,start_new_session=True)
    try:
        code=process.wait(timeout=args.seconds)
    except subprocess.TimeoutExpired:
        process.send_signal(signal.SIGTERM)
        try:
            code=process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);code=process.wait();forced=True
status_path=control/'status.txt'
runtime_status=dict(line.split('=',1) for line in status_path.read_text().splitlines() if '=' in line) if status_path.exists() else {}
text=log.read_text(errors='replace')
match=re.search(r'\[staticrecomp\] shutdown: native=(\d+) fallback=(\d+) native_exc=(\d+) hook_fb=(\d+) smc_failed=(\d+)',text)
summary={'command':command,'runtime_status':runtime_status,'exit_code':code,'forced_kill':forced,'headless':args.headless,'log':str(log),'native_statistics':dict(zip(('native','fallback','native_exceptions','hook_fallback','smc_failed'),map(int,match.groups()))) if match else None,'visual_validation':'not performed by this script','game_completion':'not tested'}
log.with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
raise SystemExit(0 if code==0 and match and int(match[1])>0 and int(runtime_status.get('frame_count','0'))>0 else 1)
