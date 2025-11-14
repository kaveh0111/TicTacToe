"""
this is an observer class for game engine
it is passed as a parameter to the Gameengine
using it other systems such as UI, voice etc. subscribes and get notifications of GameEngine
"""
from abc import ABC
from typing import List
from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def getSubjectList(self):
        #returns a list of subscription subjects
        raise NotImplementedErrors

    @abstractmethod
    def subscribeAll(self):
        raise NotImplementedError

    @abstractmethod
    def unSubscribeAll(self):
        raise NotImplementedError

    @abstractmethod
    def subscribeTo(self):
        #subscribing to a specific subject
        raise NotImplementedError

    @abstractmethod
    def unSubscribeFrom(self):
        #unsubscribe from a specific subject
        raise NotImplementedError