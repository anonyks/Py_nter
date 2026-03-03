# Base class that all drawing tools inherit from.

# ABC and abstractmethod force every tool to have the required methods.
# If a tool forgets to define draw/handle_events/preview, Python will throw an error.
from abc import ABC, abstractmethod
import pygame


class Tool(ABC):
    # Base class for all tools.
    # Every tool must have draw(), handle_events() and preview() methods.

    @abstractmethod
    def draw(self, surface):
        # Draw onto the canvas.
        ...

    @abstractmethod
    def handle_events(self, event):
        # Handle mouse and keyboard events.
        ...

    @abstractmethod
    def preview(self, screen):
        # Draw a live preview (not saved to canvas yet).
        ...
