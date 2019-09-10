import sys
import os 

sys.path.append('./')

from src.application import app

if __name__ == '__main__':
    pathDir = './test/scenarios'
    scenariosFiles = os.listdir(pathDir)

    for scenarioFilename in scenariosFiles:
        print('=== Running Scenario file {} ==='.format(scenarioFilename))

        with open(pathDir + '/' + scenarioFilename, 'r') as scenarioFile:
            sys.stdin = scenarioFile
            app.main()
            