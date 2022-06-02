#!/usr/bin/python
import linuxcnc, hal, time

lube = hal.component("WaysLube")
lube.newpin("run", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("rest", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("fault-lowlevel", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("fault-pump", hal.HAL_BIT, hal.HAL_OUT)
lube.newpin("reset", hal.HAL_BIT, hal.HAL_IN)
lube.newpin("motion", hal.HAL_FLOAT, hal.HAL_IN)
lube.newpin("machine-status", hal.HAL_BIT, hal.HAL_IN)
lube.newpin("lube-tank-level-ok", hal.HAL_BIT, hal.HAL_IN) # input from lube tank level, false means low level
lube.newpin("count", hal.HAL_S32, hal.HAL_IN)              # input from external shots counter
lube.newpin("reset-count", hal.HAL_BIT, hal.HAL_OUT)       # output to reset external shots counter
lube.newparam("on-shots", hal.HAL_U32, hal.HAL_RW)         # desired number of oil shots per cycle
lube.newparam("on-shots-timeout", hal.HAL_U32, hal.HAL_RW) # timout to detect the number of oil shots in secs
lube.newparam("off-time", hal.HAL_U32, hal.HAL_RW)         # desired off time in secs
lube.newpin("run-one-cycle", hal.HAL_BIT, hal.HAL_IN)      # input to running one cycle now
lube.newpin("disable-cycle", hal.HAL_BIT, hal.HAL_IN)      # input to disable the ways lube cycle
lube.newpin("cycle-timer", hal.HAL_U32, hal.HAL_OUT)       # output to reset external shots counter
lube.ready()

#initialize variables
lube['run'], lube['fault-lowlevel'], lube['fault-pump'] = 0, 0, 0;
try:
    if (not lube['on-shots']):
      lube['on-shots'] = 5;

    if (not lube['on-shots-timeout']):
      lube['on-shots-timeout'] = 5;
    
    if (not lube['off-time']):
      lube['off-time'] = 1000;

    while 1:
        time.sleep(1)
        lube['rest'] = 0
        lube['reset-count'] = 0;

        #1. machine needs to be on
        #2. there must me motion
        #3. there should be no pump faults
        if((not lube['disable-cycle'] or lube['run-one-cycle']) and (lube['machine-status'] or lube['run-one-cycle']) and not lube['fault-lowlevel'] and not lube ['fault-pump']):
            if(not lube['lube-tank-level-ok']):
                lube['run'] = 0; #shut off pump immediately
                lube['fault-lowlevel'] = 1; # lube tank level not ok
            else:
               if (lube['motion']>0):
                 lube['cycle-timer']=lube['cycle-timer']+1; # add one second
               if (lube['cycle-timer'] >= lube['off-time'] or lube['run-one-cycle']) :
                 #lube['run-one-cycle']=0;
                 lube['cycle-timer']=0;
                 lube['run'] = 1;
                 timeout=lube['on-shots-timeout'];
                 timeout_start = time.time();
                 while ((time.time()-timeout_start)<timeout) :
                   time.sleep(0.5)    # prevent 100% CPU load
                   if (lube['count'] >= lube['on-shots']):
                     lube['run'] = 0; #shut off pump immediately
                     lube['rest'] = 1; #show that pump is resting
                     lube['reset-count'] = 1;
                     break
                 if (lube['count'] < lube['on-shots']):
                   lube['run'] = 0; #shut off pump immediately
                   lube['fault-pump'] = 1; # pump counter not signaling
        #gives user to ability to reset the fault after fluid was filled or leak was fixed
        if(lube['reset']):
            lube['cycle-timer']=0;
            #lube['run-one-cycle']=0;
            lube['fault-lowlevel'] = 0;
            lube['fault-pump'] = 0;
            lube['reset'] = 0; #reset the reset!

except KeyboardInterrupt:
    raise SystemExit

