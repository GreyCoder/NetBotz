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
    """Netbotz Class requires IP, Username, Password"""
    def __init__(self, ip, username, password):
        self.url = 'https://%s/cgi-bin/nbSensorWebServices?wsdl' % ip
        self.location = 'https://%s/cgi-bin/nbSensorWebServices' % ip
        self.credentials = dict(username=username, password=password)
        self.t = HttpAuthenticated(**self.credentials)
        self.client = Client(self.url, location=self.location, transport=self.t)
        self.sensors = {}
        self.sensors['environment'] = {}
        for pod in self.client.service.getAllPodIDs()[0]:
            self.podLocation = self.client.service.getPod(pod)['Label']
            if len(self.client.service.getAllNumSensorIDsForPod(pod)) != 0:
                self.sensors['environment'][self.podLocation] = {}
                #self.sensors['environment'] = {podLocation}
                #self.sensors['environment'] = {}
                
                for sensorndx in self.client.service.getAllNumSensorIDsForPod(pod)[0]:
                    self.sensors['environment'][self.podLocation][sensorndx] = self.client.service.getNumSensor(sensorndx)['Value']

    def nb_report(self):
        for pod in self.client.service.getAllPodIDs()[0]:
            podLocation = self.client.service.getPod(pod)['Label']

            print "\n" + podLocation
            if len(self.client.service.getAllNumSensorIDsForPod(pod)) != 0:
                print "    Environment Sensors"
                for sensorndx in self.client.service.getAllNumSensorIDsForPod(pod)[0]:
                    print "        " + sensorndx + " = " + \
                    str(self.client.service.getNumSensor(sensorndx)['Value'])
            if len(self.client.service.getAllStateSensorIDsForPod(pod)) != 0:
                print "    State Sensors"
                for sensorndx in self.client.service.getAllStateSensorIDsForPod(pod)[0]:
                    print "        " + sensorndx + " = " + \
                    str(self.client.service.getStateSensor(sensorndx)['ValueIndex'])
