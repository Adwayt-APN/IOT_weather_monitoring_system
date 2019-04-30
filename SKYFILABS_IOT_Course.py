import sys
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import urllib2
import smtplib
from email.mime.text import MIMEText

USERNAME = "sender@gmail.com"
PASSWORD = "password"
MAILTO  = "reciever@gmail.com"



def getSensorData():

        RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    # return dict

        return (str(RH), str(T))
        RH,T= Adafruit_DHT.getSensorData()
#main() function
def main():
    # use sys.argv if needed
        if len(sys.argv) < 2:
                print('Usage: python weather_monitor.py PRIVATE_KEY')
                exit(0)
        print 'Starting...'
        baseURL = 'https://api.thingspeak.com/update?api_key=%s'% sys.argv[1]

        while True:
                try:
                         RH,T = getSensorData()
                         req = urllib2.Request(url=baseURL+'&field2=%s&field1=%s'%(RH,T))
                         f = urllib2.urlopen(req)
                         print f.read()
                         print("Humidity" +str(RH)+ " %")
                         print("Temperature" +str(T)+ "C")
                         msg = MIMEText('Temperature%s Humidity%s/n For Data Logger Click link https://thingspeak.com/channels/<key>' %(T,RH))
                         msg['Subject'] = 'Weather Report'
                         msg['From'] = USERNAME
                         msg['To'] = MAILTO

                         server = smtplib.SMTP('smtp.gmail.com:587')
                         server.ehlo_or_helo_if_needed()
                         server.starttls()
                         server.ehlo_or_helo_if_needed()
                         server.login(USERNAME,PASSWORD)
                         server.sendmail(USERNAME,MAILTO,msg.as_string())
                         server.quit()
                         f.close()
                         sleep(15)
                except:
                         print 'Exiting.'
                         break

# call main
if __name__ == '__main__':
    main()

