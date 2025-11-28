"""
 I will create a button class to create a button to play the game. 

"""
import pygame.font

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """A play button centered on the screen."""
    def __init__(self, game: 'AlienInvasion', msg: str):
        """Initialize the button with a message.
        
        Args:
            game: Reference to the main AlienInvasion instance.
            msg: Text to display on the button.
        """
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        # Create button rect centered on screen
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.screen.get_rect().center
        # Create font and render message
        self.font = pygame.font.Font(str(self.settings.font_file), self.settings.button_font_size)
        self._prep_msg(msg)

    def _prep_msg(self, msg: str):
        """Render the button message and center it inside the button rect."""
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button rectangle and the message text."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos) -> bool:
        """Return True if the mouse position is inside the button rect."""
        return self.rect.collidepoint(mouse_pos)





