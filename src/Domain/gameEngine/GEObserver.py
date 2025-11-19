from Domain.gameEngine.events import GameEvent
from typing import Callable, Optional, Type

EventHandler = Callable[[GameEvent], None]

class Observer:
    """
    GameEngine observer (publisher):
    Has exactly ONE subscriber, the Application Observer.
    """
    def __init__(self) -> None:
        self._subscriber: Optional[EventHandler] = None

    def setSubscriber(self, handler: EventHandler) -> None:
        print("Gameengine Observer: setSubscriber")
        self._subscriber = handler
        if handler is None:
            raise ValueError("GameEngine.Observer.setSubscriber: handler is None")

        self._subscriber = handler


    def notify(self, event: GameEvent) -> None:
        """
        Forward event to the subscriber.
        GameEngine will call this whenever something happens
        (TurnChanged, GameFinished, etc.).
        """
        print("gameengine Observer: notify................................", event)
        if self._subscriber is None:
            return

        self._subscriber(event)
