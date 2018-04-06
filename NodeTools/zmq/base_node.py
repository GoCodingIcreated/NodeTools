import zmq
import logging


class BaseNode(object):

    repeat_socket = None

    def __init__(self, iname, port, node_id=None):
        self.node_id = node_id

        self.context = zmq.Context()
        self.poller = zmq.Poller()

        self.should_continue = True
        self.control_socket = self.context.socket(zmq.PAIR)
        self.control_socket.bind('tcp://{}:{}'.format(iname, port))
        self.poller.register(self.control_socket, zmq.POLLIN)

    def __del__(self):
        # ToDo
        pass

    def node_id(self):
        return self.node_id

    def connect_next_node(self, next_ip, next_port):
        self.repeat_socket = self.context.socket(zmq.PAIR)
        self.repeat_socket.connect('tcp://{}:{}'.format(next_ip, next_port))
        self.poller.register(self.repeat_socket, zmq.POLLIN)

    def _process_message(self, msg):
        raise NotImplementedError

    @staticmethod
    def _extract_src_id(msg):
        return msg.split(' ')[1]

    @staticmethod
    def _extract_dst_id(msg):
        return msg.split(' ')[0]

    def _is_my_message(self, msg):
        return self._extract_dst_id(msg) == self.node_id()

    def __recv(self, socket, next_socket):
        try:
            msg = socket.recv_string()
        except zmq.ZMQError as e:
            logging.error('recv error - {}'.format(str(e)))
        else:
            if self._is_my_message(msg):
                logging.info('got message')
                self._process_message(msg)
            else:
                logging.info('forward message to [{}]'
                             .format(self._extract_dst_id(msg)))
                if next_socket is not None:
                    next_socket.send_string(msg)
                else:
                    logging.warn('cannot forward message')

    def _control_recv(self):
        return self.__recv(self.control_socket, self.repeat_socket)

    def _repeat_recv(self):
        return self.__recv(self.repeat_socket, self.control_socket)

    def message_loop(self):
        while self.should_continue:
            try:
                socket_events = dict(self.poller.poll())
            except KeyboardInterrupt:
                self.should_continue = False
                break
            else:
                if self.control_socket in socket_events:
                    self._control_recv()

                if (self.repeat_socket is not None and
                        self.repeat_socket in socket_events):
                    self._repeat_recv()
