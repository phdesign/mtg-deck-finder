from abc import ABC, abstractmethod

class DeckReaderBase(ABC):
    @abstractmethod
    def can_read(self):
        pass

    @abstractmethod
    def read(self):
        pass
