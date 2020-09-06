# Read input without requiring a new line character
# Getch class was sourced from https://code.activestate.com/recipes/134892/
class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch()


# Read the HelloWorld.xml, this gives us the x and y coordinates required to display hello world

helloWorldArray = []
discoveredWordArray = []
from bs4 import BeautifulSoup

# Read the file
xmlFile = open("HelloWorld.xml","r")
soup = BeautifulSoup(xmlFile.read(),'lxml')

x=0
# Iterate through it
for allItems in soup.find_all("items"):
    helloWorldArray.append([])
    discoveredWordArray.append([])
    for eachItem in allItems.find_all("item"):
        helloWorldArray[x].append(eachItem.contents[0])
        discoveredWordArray[x].append(" ")
    x = x + 1

def displayHelloWorld():
    for r in discoveredWordArray:
        for c in r:
            print(c,end = " ")
        print()

playerX = 0
playerY = 0

input = "w"
def setAreaVisible(x,y):
    if len(helloWorldArray) > y and y >= 0 and len(helloWorldArray[0]) > x and x >= 0:
        discoveredWordArray[y][x] = helloWorldArray[y][x]

while input == "w" or input == "a" or input == "s" or input == "d":
    if input == "w":
        playerY = max(0, playerY - 1) 
    elif input == "a":
        playerX = max(0, playerX - 1) 
    elif input == "s":
        playerY = min(len(helloWorldArray) - 1, playerY + 1) 
    elif input == "d":
        playerX = min(len(helloWorldArray[0]) - 1, playerX + 1) 
    setAreaVisible(playerX+0,playerY+1)
    setAreaVisible(playerX+0,playerY-1)
    setAreaVisible(playerX+1,playerY+0)
    setAreaVisible(playerX-1,playerY+0)
    discoveredWordArray[playerY][playerX] = "X"
    displayHelloWorld()
    input = getch().decode("utf-8").lower()

