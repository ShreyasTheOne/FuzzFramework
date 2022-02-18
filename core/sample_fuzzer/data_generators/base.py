from abc import ABC, abstractmethod


class BaseDataGenerator(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate(self):
        pass
