import socket,sys,logging,multiprocessing,uuid,os
from multiprocessing import Queue,Process,Lock
from concurrent.futures import ThreadPoolExecutor
import tensorflow as tf
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
from urllib import request

logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
        level=logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s")
logger= logging.getLogger()
ch=logging.StreamHandler()
ch.setFormatter(formatter)

def run_client(received,graph_0,model_0,image_thread):
    data = received[0].recv(2048)
    data = data.decode("utf-8")
    data = data[:data.find('[END]')]
    url = data
    logger.info("Received Client %s" % str(received[1]))
    logging.info("Client submitted URL %s" % url)
    with graph_0.as_default():
        temp = uuid.uuid1()
        logging.info("Image saved to %s/%s.jpg" % (image_thread,temp))
        img = image.load_img(request.urlretrieve(url, "%s/%s.jpg" % (image_thread,temp))[0], target_size=(227, 227))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model_0.predict(x)
        result = decode_predictions(preds)[0][0][1:]

    logging.info("SqueezeNet result: %s" % str(result))

    received[0].sendall(str(result).encode("utf-8"))

    logging.info("Client connection closed")
    received[0].shutdown(socket.SHUT_RDWR)
    received[0].close()

def handle_client(queue_client,lock,image_pro):

    graph = tf.get_default_graph()
    model = SqueezeNet()
    # creat thread pool
    executor=ThreadPoolExecutor(max_workers=4)

    while True:
        lock.acquire()
        if(queue_client.empty()==False):
            sent = queue_client.get()
            lock.release()
        else:
            lock.release()
            continue
        executor.submit(run_client,sent,graph,model,image_pro)

if __name__=='__main__':

    imagedir = os.getcwd()
    imagedir += "/images"
    if not os.path.exists(imagedir):
        os.mkdir(imagedir)

    # create an INET socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get port number and number of processes
    port = sys.argv[1]
    num_pro = sys.argv[2]

    server_socket.bind(("localhost", int(port)))
    logging.info("Start listening for connections on port %s" % port)
    # Listen for incoming connections from clients
    server_socket.listen(100)

    #creat queue
    q = Queue()
    lock=Lock()
    #creat processes
    for i in range(4):
        p = Process(target=handle_client, args=(q,lock,imagedir))
        logger.info("Created process %s" % p.name)
        p.start()

    #get client socket
    while True:
        (client_socket,address)=server_socket.accept()
        lock.acquire()
        logger.info("Client %s connected." % str(address))
        if(q.full()==False):
            q.put((client_socket,address))
            lock.release()
        else:
            lock.release()
            continue