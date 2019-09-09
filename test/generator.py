import random
import string
from datetime import datetime

def randomString(stringLength=10):
    ''' Generate a random string of fixed length 
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

pathDir = './test/scenarios/'
numberOfLines = 10000
with open(pathDir + 'Generated({})'.format(randomString(10)), 'w') as newFile:
    newFile.writelines('{ "account": { "activeCard": true, "availableLimit": 10000 } }\n')
    for i in range(numberOfLines):
        newFile.writelines('{ "transaction": { "merchant": "' + str(randomString(10)) +
                                           '", "amount": ' + str(random.randint(1,20)) + 
                                            ', "time": "' + datetime.fromtimestamp(1567992012 + random.randint(30, 40)*i).isoformat() + '.000Z" } }\n')
