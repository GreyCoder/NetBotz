from suds.client import Client
from suds.transport.https import HttpAuthenticated
"""This is a module to get data from a Netbotz device.
currently it is only a function but I will abstract it to
a class definition in the future so that you will have a
netbotz object
"""
__version__ = '.00'


def nb_report(ip, uname, pw):
    """Function to access wsdl information on Netbotz

    This function requires an IP, Username and Password

"""

    url = 'https://%s/cgi-bin/nbSensorWebServices?wsdl' % ip
    location = 'https://%s/cgi-bin/nbSensorWebServices' % ip
    credentials = dict(username=uname, password=pw)
    t = HttpAuthenticated(**credentials)

    client = Client(url, location=location, transport=t)

    for pod in client.service.getAllPodIDs()[0]:
        podLocation = client.service.getPod(pod)['Label']
        print "\n" + podLocation
        if len(client.service.getAllNumSensorIDsForPod(pod)) != 0:
            print "    Environment Sensors"
            for sensorndx in client.service.getAllNumSensorIDsForPod(pod)[0]:
                print "        " + sensorndx + " = " + \
                str(client.service.getNumSensor(sensorndx)['Value'])
        if len(client.service.getAllStateSensorIDsForPod(pod)) != 0:
            print "    State Sensors"
            for sensorndx in client.service.getAllStateSensorIDsForPod(pod)[0]:
                print "        " + sensorndx + " = " + \
                str(client.service.getStateSensor(sensorndx)['ValueIndex'])


class NetBotz(object):
    """Netbotz Class requires IP, Username, Password to create"""
    def __init__(self, ip, username, password):
        self.url = 'https://%s/cgi-bin/nbSensorWebServices?wsdl' % ip
        self.location = 'https://%s/cgi-bin/nbSensorWebServices' % ip
        self.credentials = dict(username=username, password=password)
        self.t = HttpAuthenticated(**self.credentials)
        self.client = Client(self.url, location=self.location, transport=self.t)
        self.sensors = {}

    def initialize_environment(self):
        """Initialize environment variables for this NetBotz object"""
        self.sensors['environment'] = {}
        for pod in self.client.service.getAllPodIDs()[0]:
            if len(self.client.service.getAllNumSensorIDsForPod(pod)) != 0:
                self.sensors['environment'][pod] = {}
                self.sensors['environment'][pod]['label'] = self.client.service.getPod(pod)['Label']
                for sensor in self.client.service.getAllNumSensorIDsForPod(pod)[0]:
                    self.sensors['environment'][pod][sensor] = self.client.service.getNumSensor(sensor)['Value']

    def initialize_state(self):
        """Initialize state variables for this NetBotz object"""
        self.sensors['state'] = {}
        for pod in self.client.service.getAllPodIDs()[0]:
            self.podLocation = self.client.service.getPod(pod)['Label']
            if len(self.client.service.getAllStateSensorIDsForPod(pod)) != 0:
                self.sensors['state'][pod] = {}
                self.sensors['state'][pod]['label'] = self.client.service.getPod(pod)['Label']
                for sensor in self.client.service.getAllStateSensorIDsForPod(pod)[0]:
                    self.sensors['state'][pod][sensor] = self.client.service.getStateSensor(sensor)['ValueIndex']

    def initialize_all(self):
        """Initialize all variables for this NetBotz object"""
        self.initialize_state()
        self.initialize_state()

    def initialize(self, sensortype='all'):
        if (sensortype == 'environment' or sensortype == 'e'):
            self.initialize_environment()
        elif (sensortype == 'state' or sensortype =='s'):
            self.initialize_state()
        elif sensortype == 'all':
            self.initialize_all()
        else:
            print "\nUnknown Sensor Type\n"

    def refresh(self, sensortype,verbose=False):
        if sensortype == 'environment':
            for pod in self.sensors['environment']:
                self.sensors['environment'][pod]['label'] = self.client.service.getPod(pod)['Label']
                for sensor in self.sensors['environment'][pod]:
                    if sensor != 'label':
                        if type(self.client.service.getNumSensor(sensor)['Value']) is not None:
                            self.sensors['environment'][pod][sensor] = self.client.service.getNumSensor(sensor)['Value']
                            if verbose == True:
                                print 'updated  ' + sensor
                        else:
                            print sensor + ' is None\n'
        if sensortype == 'state':
            for pod in self.sensors['state']:
                self.sensors['state'][pod]['label'] = self.client.service.getPod(pod)['Label']
                for sensor in self.sensors['state'][pod]:
                    if sensor != 'label':
                        if type(self.client.service.getStateSensor(sensor)['ValueIndex']) is not None:
                            self.sensors['state'][pod][sensor] = self.client.service.getStateSensor(sensor)['ValueIndex']
                            if verbose == True:
                                print 'updated  ' + sensor
                        else:
                            print sensor + ' is None\n'

    def report(self, sensortype='all'):
        if (sensortype == 'environment' or sensortype == 'e' or sensortype =='all'):
            if 'environment' in self.sensors:
                print "Environment Sensors"
                for pod in self.sensors['environment']:
                    print '    ' + self.sensors['environment'][pod]['label']
                    for sensor in self.sensors['environment'][pod]:
                        if sensor  != 'label':
                            print "        " + sensor + " = " + str(self.sensors['environment'][pod][sensor])
        if (sensortype == 'state' or sensortype == 's' or sensortype =='all'):
            if 'state' in self.sensors:
                print "State Sensors"
                for pod in self.sensors['state']:
                    print '    ' + self.sensors['state'][pod]['label']
                    for sensor in self.sensors['state'][pod]:
                        if sensor  != 'label':
                            print "        " + sensor + " = " + str(self.sensors['state'][pod][sensor])
