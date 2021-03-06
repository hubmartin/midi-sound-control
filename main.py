import rtmidi
import alsaaudio
import subprocess
import pyudev

# context = pyudev.Context()
# monitor = pyudev.Monitor.from_netlink(context)
# monitor.filter_by(subsystem='usb')

# for device in iter(monitor.poll, None):
#     if device.action == 'add':
#         print('{} connected'.format(device))
        # do something very interesting here.

# sudo apt-get install libasound2-dev
# sudo pip3 install pyalsaaudio pyudev rtmidi
# sudo apt install playerctl
# pm2 start $(pwd)/main.py --name midi --interpreter python3

midiin = rtmidi.RtMidiIn()

mixer = alsaaudio.Mixer()

def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
        print(midi.getNoteNumber())
        if(midi.getNoteNumber() == 62):
            print('G333')
            subprocess.run(["playerctl", "pause"])
        if(midi.getNoteNumber() == 67):
            print('D333')
            subprocess.run(["playerctl", "play"])
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
        if(midi.getControllerNumber() == 88):
            val = (midi.getControllerValue() / 127.0) * 100.0
            mixer.setvolume(int(val))

ports = range(midiin.getPortCount())
if ports:
    for i in ports:
        print(midiin.getPortName(i))
    print("Opening port 1!") 
    midiin.openPort(1)
    while True:
        m = midiin.getMessage(250) # some timeout in ms
        if m:
            print_message(m)
else:
    print('NO MIDI INPUT PORTS!')
