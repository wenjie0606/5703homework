import socket,sys,logging
from threading import Thread
import threading

logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
        level=logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s")
logger= logging.getLogger()
ch=logging.StreamHandler()
ch.setFormatter(formatter)

def send_url():

    # create an INET TCP socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server (change localhost to an IP address if necessary)
    try:
        soc.connect((sys.argv[1], int(sys.argv[2])))
        logging.info("Connected to server at (%s, %i)" % (sys.argv[1], int(sys.argv[2])))
    except Exception as err:
        logging.info("Cannot connect to server at (%s, %i)" % (sys.argv[1], int(sys.argv[2])))

    url = sys.argv[3].encode("utf-8") + b'[END]'

    # Send a message to the server
    try:
        soc.send(url)
        logging.info("URL sent to the server")
    except Exception as err:
        logging.info("Cannot sent to server ")


    # Receive data from the server
    data = soc.recv(2048)
    datade=data.decode("utf-8")
    logging.info("Server response: %s" % datade)

# Always close the socket after use
    soc.close()

if __name__=="__main__":

    '''threads = []
    for i in range(20):
        t = Thread(target=send_url)
        t.start()
        threads.append(t)'''

    send_url()