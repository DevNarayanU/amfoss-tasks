# LOG 


### My plan

- Learn about different kinds of process states and details needed to show
-  Understand where and how its stored
-  Code frontend and backend in using python.

### 1. Learn

Process states

- *New :  A freshly created process*
- *Running  : A process actively being worked on by the cpu.*
- *Terminate : Closed down process*
*and etc*

Details needed to show
-  *Only active processes to be shown* 
- *Process ID (PID)*
- *CPU Usage*
- *Memory Usage*
- *Total Active process Count*

Storage 
- Understood that almost all process details are stored in ```home/proc/``` itself.
- PID taken from its folder name which is actually its PID if its an integer
- A PID folder contains ```/comm && /stat && /statm``` areas which contains its pocess_name && CPU usage && Memory_taken respectively


Decided to use python+curses workflow

### Code

code syntaxes 
```stdscr(row,columns,str) :: used to show output in standard screen

stdscr.refresh() :: refreshes such that the things drawn are displayed then

stdscr.getmaxyx() :: returns a list with [height,width] values of your terminal screen

curses.noecho() :: doesn't show whatever to type on the canvas of terminal

curses.cbreak() :: makes sure that the input is received just the moment you type it ,*without waiting to press eneter*

stdscr.getch() :: fetches input from user and converts it into ASCII (i guess)

stdscr.nodelay() :: since getch() is being implemented it will block once it reaches that part of the code , to prevent that we  implemented nodelay().

stdscr.keypad(True) :: to accept key inputs

curses.wrapper() :: simplifies your code by allowing you to leave the code after implementing it ( we dont need to close anything due to this)




```



