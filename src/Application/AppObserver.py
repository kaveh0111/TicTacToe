from abc import ABC
from Domain.gameEngine.events import GameEvent
from typing import Callable, Dict, List, Type

# A handler is simply: function(EventSubclass) -> None
EventHandler = Callable[[GameEvent], None]

#Currently UI, later other modules such as voice, networking, webAPI, etc subscribe to this class
class Observer:
    def __init__(self) -> None:
        # map: EventClass -> list of handlers
        self._handlers: Dict[Type[GameEvent], List[EventHandler]] = {}
        #print("an instance of App Observer is created")

    def subscribe(self, event_type: Type[GameEvent], handler: EventHandler) -> None:
        """Subscribe handler to a specific Event subclass."""
        print("appObserver subscribe=====================")
        self._handlers.setdefault(event_type, []).append(handler)

    def unSubscribe(self, event_type: Type[GameEvent], handler: EventHandler) -> None:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    def notify(self, event: GameEvent) -> None:
        """Call only handlers registered for this event's class."""

        handlers = self._handlers.get(type(event), [])
        print("appObserver notify", event, "and the handler is", handlers)
        #for call_back in handlers:
        for call_back in reversed(handlers):
            call_back(event)
