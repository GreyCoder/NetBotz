from suds.client import Client
from suds.transport.https import HttpAuthenticated


def nb_report(ip, uname, pw):
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
