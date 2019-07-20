import serial
import urllib2

def WritetoCSV(filename, line):
    line=line.rstrip()
    elements =line.split(',')

    #Save as CSV file:
    firsttime=0
    try:
        fd = open(filename, 'r')
    except:
        print "File doesn't exist, creating headers"
        firsttime=1

    with open(filename,'a') as fd:
        if firsttime:
            headings="Index"
            for i in range(0, len(elements)):
                headings+="Temp"+str(i+1)+","
            headings+="Blank"
            fd.write(headings+"\n")
        fd.write(line+",\n")

    fd.close()
    print "CSV appended"

# Setup serial
ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

while True:
	if ser.inWaiting():
		line=ser.readline()
		# We expect the line to be formatted as so:
		# index_integer, temp1, temp2, temp3... etc
		print ">> "+ line
		WritetoCSV('LogTempData.csv',line)

