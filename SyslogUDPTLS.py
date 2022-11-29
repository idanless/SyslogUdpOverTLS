import ssl,socket
import sys
import time
import socket
from datetime import date,datetime
import argparse

#date time\now when the script is run
today = date.today()
now = datetime.now()
today_is = today.strftime("%d/%m/%Y")
time_is = now.strftime("%H:%M:%S")

class SyslogUDPHandler():
    def __init__(self, ip='0.0.0.0', port=7777):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ipUDP = ip
        self.portudp = port
        self.listen = (self.ipUDP, self.portudp)
        self.payload = None


    def Runserver(self):
        self.sock.bind(self.listen)

    def print_text(self):
        print(self.ip,self.port,self.listen)

    def getUdpSock(self):
        while True:
            time.sleep(0.1)
            payload, client_address = self.sock.recvfrom(655536)
            self.payload = str(payload.decode()).replace('\n','')
            print(client_address,  self.payload)
    def set_ip_port(self,ip,port):
        self.ipUDP = ip
        self.portudp = port
    def outputval(self):
        print('ip',self.ipUDP,'port',self.portudp)


class SockSSL(SyslogUDPHandler):
    def __init__(self,HOST,verify,PORT):
        self.timedate = datetime.now()
        self.port = PORT
        self.host = HOST
        self.verify = verify
        self.context = ssl.create_default_context()
        if verify is not True:
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE
        self.context.load_default_certs()
        self.connection = None
        self.OpenTcp = None
        super(SockSSL, self).__init__()






    def opennSSL(self):
        print(self.host, self.port)
        self.OpenTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = self.context.wrap_socket(self.OpenTcp,server_hostname=self.host)
        try:
            self.connection.connect((self.host, self.port))
        except ssl.SSLCertVerificationError:
            print('Error','have issue with Verification SSL ' )
            input('hit key to close')
            sys.exit(1)

        while True:
            self.get_time()
            time.sleep(0.2)
            try:
                payload, client_address = self.sock.recvfrom(655536)
                self.payload = str(payload.decode()).replace('\n', '')
                print(self.timedate.strftime("%H:%M:%S"),client_address, self.payload)
                self.connection.send(self.payload.encode())
            except ssl.SSLEOFError:
                print('lost try open connection')
                self.opennSSL()
                self.connection.send(self.payload.encode())
            #input('Hit key')
            #self.getdata()
    def get_time(self):
        self.timedate = datetime.now()

    def cloeTcp(self):
        self.OpenTcp.close()



Menu = argparse.ArgumentParser(fromfile_prefix_chars='@')
Menu.add_argument('--Syslog_port', action='store', type=int,default=514,help='by default 514' )
Menu.add_argument('--IP_syslog', action='store', type=str,default='0.0.0.0',help='by default 0.0.0.0 any interface')
Menu.add_argument('--dstportSSL', action='store', type=int,required=True,help='destination port on SSL Server')
Menu.add_argument('--verifiySSL', action='store', type=str,default=True,help='if you use self signed certificate or ip for dstIP set it on false ')
Menu.add_argument('--dstIP', action='store', type=str,default=True,required=True,help='IP or Domain recommended use Domain')


args = Menu.parse_args()

print('Config',args)
if args:
    try:
        s = SockSSL(HOST=args.dstIP, PORT=args.dstportSSL, verify=args.verifiySSL)
        s.set_ip_port(ip=args.IP_syslog, port=args.Syslog_port)
        s.Runserver()
        s.opennSSL()
    except KeyboardInterrupt:
        print('Stop')


