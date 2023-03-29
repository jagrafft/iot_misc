from abc import ABC, abstractmethod
from zmq import SUB

class ZMQStreamHandler(ABC):
    """
    """
    @abstractmethod
    def __init__(self, context, address: str, sample_rate: float) -> None:
        """
        """
        self._address = address
        self._context = context
        self._sample_rate = sample_rate
        self._receiving = False

        self._socket = self._context.socket(SUB)

    # TODO Error handling, report success/fail
    @abstractmethod
    def connect(self):
        """
        """
        self._socket.connect(self._address)

    @abstractmethod
    def console_stream(self):
        """
        """
        if self._receiving:
            while True:
                print(self.sample())
        else:
            print('ERROR: receiving = False')

    @abstractmethod
    def local_stream(self):
        """
        """
        pass

    @abstractmethod
    def sample(self):
        """
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        """
        self._socket.close()
        self._context.term()
    
    @abstractmethod
    def subscribe(self, topics=''):
        """
        """
        self._socket.subscribe(topics)

    @property
    @abstractmethod
    def receiving(self) -> str:
        """
        """
        return f"""{{ 'receiving': {self._receiving} }}"""

    @receiving.setter
    @abstractmethod
    def receiving(self, flag: bool) -> None:
        """
        """
        pass

    @property
    @abstractmethod
    def sample_rate(self) -> str:
        """
        """
        return f"""{{ 'sample_rate': {self._sample_rate} }}"""

    @sample_rate.setter
    @abstractmethod
    def sample_rate(self, rate: float) -> None:
        """
        """
        pass
