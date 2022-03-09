import sys
import os
import textwrap
import curses
import json
import numpy as np
import random
import string
from pylsl import StreamInfo, StreamOutlet

from read_book import Book

from absl import flags
FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'debug')
flags.DEFINE_string('output_directory', None, 'where to save outputs')
flags.DEFINE_string('book_file', None, 'text to read')
flags.mark_flag_as_required('output_directory')
flags.mark_flag_as_required('book_file')

def display_sentence(sentence, win):
    height, width = win.getmaxyx()
    win.clear()
    wrapped_sentence = textwrap.wrap(sentence, width)
    for i, text in enumerate(wrapped_sentence):
        if i >= height:
            break
        win.addstr(i, 0, text)
    win.refresh()

def save_data(output_idx, book, silent):
    #Silent is 1 for silent, 0 for voiced
    info_file = os.path.join(FLAGS.output_directory, f'{output_idx}_info.json')

    if book is None:
        # special silence segment
        bf = ''
        bi = -1
        t = ''
    else:
        bf = book.file
        bi = book.current_index
        t = book.current_sentence()

    with open(info_file, 'w') as f:
        json.dump({'book':bf, 'silent':silent, 'sentence_index':bi, 'text':t}, f)

def main(stdscr):
    os.makedirs(FLAGS.output_directory, exist_ok=False)
    output_idx = 0

    curses.curs_set(False)
    stdscr.nodelay(True)

    text_win = curses.newwin(curses.LINES-1, curses.COLS, 0, 0)

    recording = False
    silent = 1 # Do silent first

    # LSL
    # first create a new stream info (here we set the name to MyMarkerStream,
    # the content-type to Markers, 1 channel, irregular sampling rate,
    # and string-valued data) The last value would be the locally unique
    # identifier for the stream as far as available, e.g.
    # program-scriptname-subjectnumber (you could also omit it but interrupted
    # connections wouldn't auto-recover). The important part is that the
    # content-type is set to 'Markers', because then other programs will know how
    #  to interpret the content
    info = StreamInfo('MarkersForBooks', 'Markers', 1, 0, 'string', 'uidmkrs01')
    # make an outlet
    outlet = StreamOutlet(info)

    with Book(FLAGS.book_file) as book:
        stdscr.clear()
        stdscr.addstr(0,0,'<Press any key to begin.>')
        stdscr.refresh()

        while True:
            if not recording:
                c = stdscr.getch()
                if c >= 0:
                    # keypress
                    recording = True
                    # Send marker to indicate start
                    outlet.push_sample(['Start'])

                    stdscr.addstr(curses.LINES-1, 0, "Type 'q' to quit, 'n' or ' ' for next, 'c' when complete speaking")
                    #display_sentence('<silence>', text_win)
                    stdscr.refresh()
            else:
                c = stdscr.getch()
                if c < 0:
                    # no keypress
                    pass
                elif c == ord('q'):
                    # Quit. Close save data file. Send marker to indicate end. Stop lsl.
                    outlet.push_sample(['End'])

                    break
                elif c == ord('n') or c == ord(' '):

                    if silent == 1:
                        display_sentence('<silence>', text_win)
                        #Send marker to indicate start and output index for silent
                        marker_text = 'SBegin' + str(output_idx)
                        outlet.push_sample([marker_text])

                    else: 
                        display_sentence(book.current_sentence(), text_win)
                        # Send marker to indicate start and output_idx for vocalized
                        marker_text = 'VBegin' + str(output_idx)
                        outlet.push_sample([marker_text])


                elif c == ord('c'):
                    if output_idx == 0:
                        save_data(output_idx,None, silent)
                    else:
                        save_data(output_idx, book, silent)

                    # if completed sentence, send marker to indicate complete
                    if silent == 1:
                        # Send marker for silent end of sentence
                        marker_text = 'SEnd' + str(output_idx)
                        outlet.push_sample([marker_text])

                        # Switch from silent to vocalized
                        silent = 0
                    else: 
                        
                        # Send marker for vocalized end of sentence
                        marker_text = 'VEnd' + str(output_idx)
                        outlet.push_sample([marker_text])

                        # Switch from vocalized to silent
                        silent = 1
                        # Only adance after doing silent and vocalized
                        output_idx += 1
                        book.next()
                    
FLAGS(sys.argv)
curses.wrapper(main)
