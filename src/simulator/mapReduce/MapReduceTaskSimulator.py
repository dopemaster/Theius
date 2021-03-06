import numpy
from src.Utility import getRandomElement
from src.simulator.RandomSimulator import RandomSimulator

__author__ = 'Roman'

class MapReduceTaskSimulator(RandomSimulator):
    def __init__(self, machineNames, taskName, time):
        RandomSimulator.__init__(self, [])

        self.taskName = taskName

        numberOfMapJobs = 10
        self.map = []
        for i in xrange(0, numberOfMapJobs):
            mapJob = {
                'id': i,
                'name': "%s%s%d" % (self.taskName, "-mapJob", i),
                'start': time + 0,
                'duration': int(numpy.random.normal(loc=60, scale=5)),
                'location': getRandomElement(machineNames)
            }
            if mapJob['duration'] <= 0:
                mapJob['duration'] = 1
            mapJob['end'] = int(mapJob['start'] + mapJob['duration'])
            self.map.append(mapJob)

        numberOfReduceJobs = 10
        self.reduce = []
        for i in xrange(0, numberOfReduceJobs):
            reduceJob = {
                'id': numberOfMapJobs + i,
                'name': "%s%s%d" % (self.taskName, "-reduceJob", i),
                'start': time + int(numpy.random.normal(loc=60, scale=5)),
                'duration': int(numpy.random.normal(loc=60, scale=5)),
                'location': getRandomElement(machineNames)
            }
            if reduceJob['duration'] <= 0:
                reduceJob['duration'] = 1
            reduceJob['end'] = int(reduceJob['start'] + reduceJob['duration'])
            self.reduce.append(reduceJob)

        self.time = time

    def updates(self):
        updates = RandomSimulator.updates(self)

        updates['start'] = []
        updates['end'] = []

        for mapTask in self.map:
            if mapTask['start'] == self.time:
                updates['start'].append(mapTask)
                self.addMachine(mapTask['name'])
            elif mapTask['end'] == self.time:
                updates['end'].append(mapTask)
                self.removeMachine(mapTask['name'])

        for reduceTask in self.reduce:
            if reduceTask['start'] == self.time:
                updates['start'].append(reduceTask)
                self.addMachine(reduceTask['name'])
            elif reduceTask['end'] == self.time:
                updates['end'].append(reduceTask)
                self.removeMachine(reduceTask['name'])

        self.time += 1

        return updates


    def isCompleted(self):
        for mapTask in self.map:
            if self.time <= mapTask['end']:
                return False

        for reduceTask in self.reduce:
            if self.time <= reduceTask['end']:
                return False

        return True

    def topology(self):
        currentTopology = {
            'name': self.taskName,
            'children': []
        }
        for mapTask in self.map:
            if mapTask['name'] in self.nodeState:
                currentTopology['children'].append(mapTask)
        for reduceTask in self.reduce:
            if reduceTask['name'] in self.nodeState:
                currentTopology['children'].append(reduceTask)
        return currentTopology

    def state(self):
        currentState = {}
        for mapTask in self.map:
            if mapTask['name'] in self.nodeState:
                currentState[mapTask['name']] = dict(self.nodeState[mapTask['name']].items() + mapTask.items())
        for reduceTask in self.reduce:
            if reduceTask['name'] in self.nodeState:
                currentState[reduceTask['name']] = dict(self.nodeState[reduceTask['name']].items() + reduceTask.items())
        return currentState

    def getTime(self):
        return self.time