# DMAS
Repository of our project for the course Design of Multi-Agent Systems. This simulation investigates whether social conventions naturally arise in a grid-based open world environment.

# START
1. python service/main.py  (This is the server running the simulation)
2. python non-gui.py       (Script version to call/listen agent simulation)
2. python gui.py           (GUI version to call/listen agent simulation, *needs Kivy*)

# Kivy install Ubuntu
1. sudo add-apt-repository ppa:kivy-team/kivy-daily  # Latest Kivy
2. sudo apt-get update
3. sudo apt-get upgrade
4. sudo apt-get install python-kivy  # Python 2.7

http://kivy.org/docs/installation/installation-linux.html

## Dependencies
http://kivy.org/docs/installation/installation-linux.html#installation-in-a-virtual-environment

# Git usage
## First time setup
1. git clone https://github.com/PdeRooij/DMAS.git
2. git checkout -b "name"  # Creates new branch and go to that branch

## Git cycle
1. git pull
2. *edit code*
3. git add *filename*  # -A instead of *filename* if you want to add all changes
4. git commit -m "change message here"
5. git push  # Send everything to GitHub

## Other git commands
* git merge *branch*  # To merge branch
* git checkout *branch*  # Switch to different branch if every change is checkout or undone
