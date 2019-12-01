from io import StringIO
import pandas as pd

# ' The TR3 file comes in three parts - SETTINGS, PHASES and POSITION. We separate the file as per these separating lines and thenread each appropriate text part

POSITION_SEPARATOR = "frame         roomx         roomy         arena angle   arenax        arenay        phase         pausa"
SETTINGS_SEPARATOR = "phase         cue           cueno         laser         startpoint    segments"
PHASES_SEPARATOR = "phase         sector        mode          avoid         shape         r             r0            r1            keytonext"


def read_position(path):
    file = open(path, 'r')
    lines = file.readlines()
    position_head = next((x for x in lines if POSITION_SEPARATOR in x), [None])
    i_position = [lines.index(position_head)]
    position_lines = [lines[x] for x in range(i_position[0], len(lines))]
    text = StringIO(''.join(position_lines))
    position = pd.read_fwf(text, header=0)  # reads well formated textw with fixed size but unequal things in each part
    file.close()
    return position


def read_phases(path):
    file = open(path, 'r')
    lines = file.readlines()
    position_head = next((x for x in lines if POSITION_SEPARATOR in x), [None])
    phases_head = next((x for x in lines if PHASES_SEPARATOR in x), [None])
    i_phases = [lines.index(phases_head), lines.index(position_head)-1]
    phases_lines = [lines[x] for x in range(i_phases[0], i_phases[1])]
    phases = pd.read_csv(StringIO(''.join(phases_lines)), header=0, sep='\s+')
    return phases


def read_settings(path):
    file = open(path, 'r')
    lines = file.readlines()
    phases_head = next((x for x in lines if PHASES_SEPARATOR in x), [None])
    settings_head = next((x for x in lines if SETTINGS_SEPARATOR in x), [None])
    i_block1 = [lines.index(settings_head), lines.index(phases_head)-1]
    settings_lines = [lines[x] for x in range(i_block1[0], i_block1[1])]
    settings = pd.read_csv(StringIO(''.join(settings_lines)), header=0, sep='\s+')
    return settings
