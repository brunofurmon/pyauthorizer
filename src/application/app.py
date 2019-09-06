import sys

from src.domain.command.account.createaccount import CreateAccount

def processLine(line):
    ''' Dispatches the current @line command

    Keyword arguments:
        line -- JSON formatted line containing an operation
    '''

    # Processing an account
    if '"account"' in line:
        command = CreateAccount(line)
        print("I'll process an account: {}".format(command.accountToCreate))
    # Transaction
    else:
        print("I'll process a transaction", line)

def main():
    
    # Operates each line from STDIN. Supposing the program is called as following:
    # python ./src/application/app.py < operations
    for line in sys.stdin:
        processLine(line)

if __name__ == '__main__':
    main()