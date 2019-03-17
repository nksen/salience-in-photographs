"""
--Naim Sen--
--Toby Ticehurst--

test.py
psychopy_test.py
Testing psychopy for displaying images to participants.
"""

from psychopy import visual, core, event  # import some libraries from PsychoPy

#create a window
window_xy = (1920, 1080)
mywin = visual.Window(
    window_xy, pos=(0, 0), monitor="testMonitor", fullscr=True, units="pixels")

#create some stimuli
grating = visual.GratingStim(
    win=mywin, mask="circle", size=1080, pos=[-4, 0], sf=3)
fixation = visual.GratingStim(win=mywin, size=1080, pos=[0, 0], sf=0)

#draw the stimuli and update the window
grating.draw()
#fixation.draw()
while True:
    mywin.update()

    #pause, so you get a chance to see it!
    core.wait(0.01)
    if 'escape' in event.waitKeys():
        core.quit()