from abc import ABC
from Domain.gameEngine.events import GameEvent
from typing import Callable, Dict, List, Type
import logging

# A handler is simply: function(EventSubclass) -> None
EventHandler = Callable[[GameEvent], None]

logger = logging.getLogger(__name__)

#Currently UI, later other modules such as voice, networking, webAPI, etc subscribe to this class
class Observer:
    def __init__(self) -> None:
        # map: EventClass -> list of handlers
        self._handlers: Dict[Type[GameEvent], List[EventHandler]] = {}
        # logger.debug("an instance of App Observer is created")
        logger.debug("Observer instance created")

    def subscribe(self, event_type: Type[GameEvent], handler: EventHandler) -> None:
        """Subscribe handler to a specific Event subclass."""
        logger.debug("Observer.subscribe() called for event_type=%s with handler=%s", event_type, handler)
        self._handlers.setdefault(event_type, []).append(handler)

    def unSubscribe(self, event_type: Type[GameEvent], handler: EventHandler) -> None:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)
            logger.debug("Observer.unSubscribe() removed handler=%s for event_type=%s", handler, event_type)
        else:
            logger.debug("Observer.unSubscribe() no-op: handler=%s not found for event_type=%s", handler, event_type)

    def notify(self, event: GameEvent) -> None:
        """Call only handlers registered for this event's class."""

        handlers = self._handlers.get(type(event), [])
        logger.debug("Observer.notify() event=%s, handlers=%s", event, handlers)
        #for call_back in handlers:
        for call_back in reversed(handlers):
            call_back(event)
