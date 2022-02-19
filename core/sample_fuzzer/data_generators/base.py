from abc import ABC, abstractmethod


class BaseDataGenerator(ABC):

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def generate():
        pass
