from Domain.gameEngine.events import GameEvent
from typing import Callable, Optional, Type
import logging

EventHandler = Callable[[GameEvent], None]

logger = logging.getLogger(__name__)


class Observer:
    """
    GameEngine observer (publisher):
    Has exactly ONE subscriber, the Application Observer.
    """
    def __init__(self) -> None:
        self._subscriber: Optional[EventHandler] = None

    def setSubscriber(self, handler: EventHandler) -> None:
        logger.debug("GameEngine.Observer.setSubscriber() called with handler=%s", handler)
        assert handler is not None, "GameEngine.Observer.setSubscriber: handler is None"
        self._subscriber = handler

    def notify(self, event: GameEvent) -> None:
        """
        Forward event to the subscriber.
        GameEngine will call this whenever something happens
        (TurnChanged, GameFinished, etc.).
        """
        logger.debug("GameEngine.Observer.notify() called with event=%s", event)
        if self._subscriber is None:
            return

        self._subscriber(event)
