from abc import ABC, abstractmethod


class Subject(ABC):
    @abstractmethod
    def addObserver():
        pass
    
    @abstractmethod
    def removeObserver():
        pass
    
    @abstractmethod
    def notifyObservers():
        pass


class Observer(ABC):
    @abstractmethod
    def update():
        pass
