"""
--Naim Sen--
--Toby Ticehurst--

Mar 2019

main.py

top-level script for running an experiment.

For now this will be a MVP.

Copyright © 2018, Naim Sen 
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
# Imports

from psychopy import gui

from ..apti import utilities


def get_exp_info():
    # dialog box
    exp_info = {'participant no.': '', 'date': ''}
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Exp_info')
    if dlg.OK == False:
        core.quit()


def main():
    #### initialise etc. ####

    # generate session info
    exp_info = get_exp_info()

    session_info = utilities.Bunch(
        exp_name='APTIVAL.psyexp', exp_info=exp_info)


if __name__ == "__main__":
    main()
    print("thing")
