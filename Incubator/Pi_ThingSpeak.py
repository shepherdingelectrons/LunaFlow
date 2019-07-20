import serial
import urllib2
import datetime

def num2str(num):
    n = str(num)
    if len(n)<2: n='0'+n
    return n

def ThingSpeak(line):
    baseURL = 'http://api.thingspeak.com/update?api_key=XXXXXXXXXXXXXXXX' # Note that your ThingSpeak channel API key replaces 'XXXXX...'
    filename = 'IncubatorData.csv'

    line=line.rstrip()
    elements =line.split(',')

    varstr = ""
    for i in range(0, len(elements)):
        varstr+="&field"+str(i+1)+"="+elements[i].replace(".","%2E")

    dt=datetime.datetime.now()
    date = str(dt.year)+"-"+num2str(dt.month)+"-"+num2str(dt.day)
    time = num2str(dt.hour)+":"+num2str(dt.minute)+":"+num2str(dt.second)
    print date, time, line, elements

    #post to ThingSpeak
    connectok=1
    try:
        f = urllib2.urlopen(baseURL + varstr)
        f.read()
        f.close()
    except:
        print "Could not connect, URLError"
        connectok=0

    #Save as CSV file:
    firsttime=0
    try:
        fd = open(filename, 'r')
    except:
        print "File doesn't exist, creating headers"
        firsttime=1

    with open(filename,'a') as fd:
        if firsttime:
            headings="Date and time,"
            for i in range(0, len(elements)):
                headings+="field"+str(i+1)+","
            headings+="ThingSpeak OK"
            fd.write(headings+"\n")
        fd.write(date+" "+time+","+line+","+str(connectok)+"\n")

    fd.close()
    print "CSV appended"

# Setup serial
ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

counter=0
while True:
	if ser.inWaiting():
		line=ser.readline()
		print ">> "+ str(counter)+ ":" + line
		ThingSpeak(line)
		counter+=1

