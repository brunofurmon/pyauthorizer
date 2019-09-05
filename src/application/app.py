import sys

def processLine(line):
    print(line, end="")

def main():
    
    # Operates each line from STDIN. Supposing the program is called as following:
    # python ./src/application/app.py < operations
    for line in sys.stdin:
        processLine(line)

if __name__ == '__main__':
    main()