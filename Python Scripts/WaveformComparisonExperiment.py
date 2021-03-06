# This is the script instantiated from WaveformComparisonMultiThread.py
import sys
import os
import neuron

# get the process id assigned by the master script (WaveformComparisonMultiThread.py)
processId = int(sys.argv[1])

# create a file for output
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'file'+str(processId)+'.csv')

# set standard output to the new file
sys.stdout = open(my_file, 'w')

# setup the ability to use NEURON
h = neuron.hoc.HocObject()

def hocSetup():
    global processId
    # Load NEURON with all the models and procedures normally available
    h('nrn_load_dll("L:/Work/GithubRepos/NEURON/Current Simulation/models/nrnmech.dll")')
    h('load_file("L:/Work/GithubRepos/NEURON/Current Simulation/CNOW_run.hoc")')
    # Fiber diameter varies across each process
    setDiam = 'changeDiam(' + str(processId) + ')'
    print(setDiam)
    h(setDiam)
    h('setStim(10,40,.1)')
    h('insert_cf()') # set freq-dep MRG MODEL

def setHocTimeStep(frequency):
    # Set time step value to be 1/12 the period, or smaller
    # if frequency <= 10:
    #     h('steps_per_ms = 200')
    #     h('dt = .005')
    #     print('dt,.005')
    # else:
    #     h('steps_per_ms = 1000')
    #     h('dt = .001')
    #     print('dt,.001')
    # Optional time step setting for faster less accurate trials (good for the BT tests which can run for a long time)
    # if frequency <= 15:
    #     h('steps_per_ms = 200')
    #     h('dt = .005')
    #     print('dt,.005')
    # elif frequency <= 20:
    #     h('steps_per_ms = 250')
    #     h('dt = .004') 
    #     print('dt,.004')
    # elif frequency <= 40:
    #     h('steps_per_ms = 500')
    #     h('dt = .002')
    #     print('dt,.002')
    # elif frequency <= 80:
    #     h('steps_per_ms = 1000')
    #     h('dt = .001')
    #     print('dt,.001')

    # Set dt to exactly 1/12 the period
    setSteps = 'steps_per_ms = ' + str(12 * frequency)
    h(setSteps)
    h('dt = 1/steps_per_ms')

def setTotalTime(freq):
    # this is used within the activation threshold search
    # large pulse widths (ie low frequencies) require a test simulation with a larger tstop
    if freq > 1:
        h('tstop = 7') 
    elif freq >= .25:
        h('tstop = 9')
    elif freq >= .1:
        h('tstop = 12')
    elif freq >= .05:
        h('tstop = 17')
    elif freq >= .025:
        h('tstop = 27')
    elif freq >= .016:
        h('tstop = 37')
    h('tstop_changed()')

def sineWaveTest():
    # find the block threshold (BT) for frequencies 10 to 60 kHz with 5 kHz increments
    # to narrow the search we can make a guess at what the BT is by observing that
    #   from 10 to 60 kHz the block threshold is approximately growing linearly

    # inital setup (selecting the sine waveform electrode)
    h('waveform_sel(1)')
    h('onset1 = 10')
    h('dur1 = 300')
    h('setoffset(0)')
    h('sinestim()')
    print("SINE WAVE")

    # Find <10kHz Block
    for i in range(3,10,1):
        print('FREQUENCY,'+str(i*1000))
        h('freq = '+str(i*1000))
        h('sinestim()') # make sure to update the electrode parameters
        setHocTimeStep(i)   # dont forget to make sure an appropriate time step is used!
        command = 'findThreshold(101000,600000,0,10,50,.1,1,1000)'
        h(command)

    # Find 10kHz Block
    print('FREQUENCY,'+str(10000))
    h('freq = '+str(10000))
    h('sinestim()') # make sure to update the electrode parameters
    setHocTimeStep(10)  # dont forget to make sure an appropriate time step is used!
    h('block10kHz = findThreshold(301000,800000,0,10,50,.1,1,1000)')
    # Find 60kHz Block
    print('FREQUENCY,'+str(60000))
    h('freq = '+str(60000))
    h('sinestim()') # make sure to update the electrode parameters
    setHocTimeStep(60)  # dont forget to make sure an appropriate time step is used!
    h('block60kHz = findThreshold(401000,1300000,0,10,50,.1,1,1000)')

    # using these two block values we can guess at the BT in between 10 and 60kHz
    block10 = h.block10kHz
    block60 = h.block60kHz

    for i in range(15,60,5):
        print('FREQUENCY,'+str(i*1000))
        h('freq = '+str(i*1000))
        h('sinestim()') # make sure to update the electrode parameters
        setHocTimeStep(i)   # dont forget to make sure an appropriate time step is used!
        minAmp = (block60-block10)/50000*i*1000+(block10-(block60-block10)/(50000)) - 200000
        maxAmp = minAmp + 400000
        print("MIN AMP,"+str(minAmp))
        print("MAX AMP,"+str(maxAmp))
        command = 'findThreshold('+str(minAmp)+','+str(maxAmp)+',0,10,50,.1,1,1000)'
        h(command)

def triWaveTest():
    # find the block threshold (BT) for frequencies 10 to 60 kHz with 5 kHz increments
    # to narrow the search we can make a guess at what the BT is by observing that
    #   from 10 to 60 kHz the block threshold is approximately growing linearly

    # select the triangle waveform electrode
    h('waveform_sel(2)')
    h('amp1 = 1500000')
    h('onset1 = 10')
    h('dur1 = 300')
    h('offset = 0')
    h('tristim()')  # make sure to update the electrode parameters
    print("TRIANGLE WAVE")

     # Find <10kHz Block
    for i in range(3,10,1):
        print('FREQUENCY,'+str(i*1000))
        h('freq = '+str(i*1000))
        h('tristim()') # make sure to update the electrode parameters
        setHocTimeStep(i)   # dont forget to make sure an appropriate time step is used!
        command = 'findThreshold(301000,1000000,0,10,50,.1,1,1000)'
        h(command)


    # Find 10kHz Block
    print('FREQUENCY,'+str(10000))
    h('freq = '+str(10000))
    h('tristim()')
    setHocTimeStep(10)  # dont forget to make sure an appropriate time step is used!
    h('block10kHz = findThreshold(401000,1000000,0,10,50,.1,1,1000)')
    # Find 60kHz Block
    print('FREQUENCY,'+str(60000))
    h('freq = '+str(60000))
    h('tristim()')
    setHocTimeStep(60)  # dont forget to make sure an appropriate time step is used!
    h('block60kHz = findThreshold(600000,2000000,0,10,50,.1,1,1000)')

    # using these two variables we can guess the BT for the values in between
    block10 = h.block10kHz
    block60 = h.block60kHz

    for i in range(15,60,5):
        print('FREQUENCY,'+str(i*1000))
        h('freq = '+str(i*1000))
        h('tristim()')  # make sure to update the electrode parameters
        setHocTimeStep(i)   # dont forget to make sure an appropriate time step is used!
        minAmp = (block60-block10)/50000*i*1000+(block10-(block60-block10)/(50000)) - 200000
        maxAmp = minAmp + 400000
        print("MIN AMP,"+str(minAmp))
        print("MAX AMP,"+str(maxAmp))
        command = 'findThreshold('+str(minAmp)+','+str(maxAmp)+',0,10,50,.1,1,1000)'
        h(command)

def setSquareWaveParams(frequency):
    cathodDuration = 1/frequency/2
    setCathodDur = 'cathod_dur=' + str(cathodDuration)
    setPostCathodDur = 'postCathod_dur=0'
    setAnodDur = 'anod_dur=' + str(cathodDuration)
    setPostAnodDur = 'postAnod_dur=0'
    h(setCathodDur)
    h(setPostCathodDur)
    h(setAnodDur)
    h(setPostAnodDur)

def squareWaveTest():
    # find the block threshold (BT) for frequencies 10 to 60 kHz with 5 kHz increments
    # to narrow the search we can make a guess at what the BT is by observing that
    #   from 10 to 60 kHz the block threshold is approximately growing linearly

    # select the square wave electrode
    h('waveform_sel(0)')
    # Set the square wave params to match the frequency

    for i in range(3,10,1):
        print('FREQUENCY,'+str(i*1000))
        frequency = i
        setSquareWaveParams(frequency)
        setHocTimeStep(i)
        command = 'findThreshold(200000,700000,0,10,50,.1,1,1000)'
        h(command)

     # Find 10kHz Block
    print('FREQUENCY,'+str(10000))
    frequency = 10
    setSquareWaveParams(frequency)
    setHocTimeStep(10)
    h('block10kHz = findThreshold(100000,1000000,0,10,50,.1,1,1000)')
    # Find 60kHz Block
    print('FREQUENCY,'+str(60000))
    frequency = 60
    setSquareWaveParams(frequency)
    setHocTimeStep(60)
    h('block60kHz = findThreshold(300000,1500000,0,10,50,.1,1,1000)')
    block10 = h.block10kHz
    block60 = h.block60kHz

    for i in range(15,60,5):
        print('FREQUENCY,'+str(i*1000))
        frequency = i
        setSquareWaveParams(frequency)
        setHocTimeStep(i)
        minAmp = (block60-block10)/50000*i*1000+(block10-(block60-block10)/(50000)) - 200000
        maxAmp = minAmp + 400000
        print("MIN AMP,"+str(minAmp))
        print("MAX AMP,"+str(maxAmp))
        command = 'findThreshold('+str(minAmp)+','+str(maxAmp)+',0,10,50,.1,1,1000)'
        h(command)


def activationTest():
    # this will test all 3 waves because it should be a quick test
    # first sine wave
    h('waveform_sel(1)')
    h('setoffset(0)')
    h('sinestim()')
    print("SINE WAVE")
    for freq in [60,55,50,45,40,35,30,25,20,15,10,9,8,7,6,5,4,3,2,1,.5, .25, .1, .05, .025, .01666]:
        print('Frequency,'  + str(freq*1000))
        print('Pulse Width,' + str(1/(freq*2)))
        h('freq = '+str(freq*1000))
        h('sinestim()')
        setTotalTime(freq)
        setHocTimeStep(freq)
        command = 'stdurationFinder(0,-1000000,1000,1/(' + str(freq*2) + '))'
        h(command)

    # triangle wave
    h('waveform_sel(2)')
    h('offset = 0')
    h('tristim()')
    print("TRIANGLE WAVE")
    for freq in [60,55,50,45,40,35,30,25,20,15,10,9,8,7,6,5,4,3,2,1,.5, .25, .1, .05, .025, .01666]:
        print('FREQUENCY,'+str(freq*1000))
        print('Pulse Width,' + str(1/(freq*2)))
        h('freq = '+str(freq*1000))
        h('tristim()')
        setTotalTime(freq)
        setHocTimeStep(freq)
        command = 'stdurationFinder(0,-1000000,1000,1/(' + str(freq*2) + '))'
        h(command)

    # square wave
    h('waveform_sel(0)')
    print("SQUARE WAVE")
    # Set the square wave params to match the frequency print("TRIANGLE WAVE")
    for freq in [60,55,50,45,40,35,30,25,20,15,10,9,8,7,6,5,4,3,2,1,.5, .25, .1, .05, .025, .01666]:
        print('FREQUENCY,'+str(freq*1000))
        print('Pulse Width,' + str(1/(freq*2)))
        setSquareWaveParams(freq)
        command = 'stdurationFinder(0,-1000000,1000,1/(' + str(freq*2) + '))'
        h(command)

hocSetup()
triWaveTest()