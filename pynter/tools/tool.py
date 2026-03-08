# base class that all tools inherit from

# ABC and abstractmethod force every tool to have the required methods
# if a tool forgets to define draw/handle_events/preview python will throw an error
from abc import ABC, abstractmethod
import pygame


class Tool(ABC):
    # every tool must have draw(), handle_events() and preview()

    @abstractmethod
    def draw(self, surface):
        # draw onto the canvas
        ...  # ellipsis works like pass here, just a placeholder for abstract methods

    @abstractmethod
    def handle_events(self, event):
        # handle mouse and keyboard events
        ...

    @abstractmethod
    def preview(self, screen):
        # live preview (not saved to canvas yet)
        ...
