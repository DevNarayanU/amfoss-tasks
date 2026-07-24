from pathlib import Path
import time;
import curses;
from curses import wrapper

def process_info(stdscr):
    proc = Path("/proc")
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    row = 2
    stdscr.addstr(0, 0, "PID")
    stdscr.addstr(0, 10, "Process Name")
    stdscr.addstr(0,50, "CPU Usage(ticks)")
    stdscr.addstr(0,70, "Memory Usage")
    height= stdscr.getmaxyx()[0]
    for i in proc.iterdir():
        if row>=height-1:
            break
        
        if i.is_dir() and i.name.isdigit():
            try:
                with open(i/"comm") as f:
                        name= f.read().strip()
                with open(i/"stat") as f:
                        stat = f.read().split()
                with open(i/"statm") as f:
                        ram= f.read().split()
                        raminkb= int(ram[1])*4

                stdscr.addstr(row,0,i.name)
                stdscr.addstr(row,10,name)
                stdscr.addstr(row,50,stat[13])
                stdscr.addstr(row,70,f"{raminkb} kB")
                
                row+=1
            except (PermissionError, FileNotFoundError):
                continue
    stdscr.refresh()

       


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        stdscr.clear()
        process_info(stdscr)
        stdscr.refresh()
        stdscr.addstr(stdscr.getmaxyx()[0]-1, 0, "Press 'q' to exit::  ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
             break
        time.sleep(0.5)

wrapper(main)