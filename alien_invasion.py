import sys
import pygame
from setting import Settings
from game_stat import GameStat
from ship import Ship
from arsenal import Arsenal
from alien import Alien
from alien_fleet_file import AlienFleet
from button import Button
from time import sleep
from hud import HUD


class AlienInvasion:
    """Main class that manages the game assets and behavior.""" 
    def __init__(self):
        """Prepare the game and create initial game resources.

        Initializes pygame, loads settings and assets, sets up the
        display and sounds, and creates the player ship and alien fleet.

        """
        pygame.init()
        self.settings = Settings()


        self.settings.initialize_dynamic_settings()
        # track game status (ships left, active state, etc.)

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))

        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
                                         (self.settings.screen_w, self.settings.screen_h)
            )

    
        self.game_stat = GameStat(self)
        self.HUD = HUD(self)


        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact = pygame.mixer.Sound(self.settings.impact)
        self.impact.set_volume(0.7)





        self.ship = Ship(self, Arsenal(self))

        self.alien_fleet= AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.game_active = False
        
        # Create the play button
        self.play_button = Button(self, 'Play')

        


        

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.ship.arsenal.update_arsenal() # Changed from .update() to .update_arsenal()
                self.alien_fleet.update_fleet()
                self._check_collisions()
                self.HUD.update_scores()
            self._update_screen()
            self.clock.tick(60) # Limit frame rate to 60 FPS



    
    def _check_collisions(self):
        """Detect and handle collisions between game objects.

        - If the ship collides with any alien, update game status.
        - If the fleet reaches the bottom, update game status.
        - If bullets hit aliens, play impact sound and remove them.
        """
        # check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self.check_games_status()

        # reset the game stats
        self.game_stat.reset_stats()



        # check collisions for aliens and bottom of the screen
        if self.alien_fleet.check_fleet_bottom():
            # call the handler to update ships/level when fleet reaches bottom
            self.check_games_status()





        # check collision of alien and projectiles. 

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact.play()
            self.impact.fadeout(500)
            self.game_stat.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()   
            self.settings.increase_difficulty()
            
            # update game status level

            self.game_stat.update_level()
            # update HUD View




           
    def check_games_status(self):
        """Update remaining ships and either reset the level or end the game.

        If ships remain, decrement the counter, reset the level and pause
        briefly. If no ships remain, set the game to inactive so updates stop.
        """
        if self.game_stat.ship_limit > 0:
            self.game_stat.ship_limit -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self):
        """Clear bullets and aliens and recreate the alien fleet.

        Called when the player loses a ship or the level is restarted.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()


    def restart_game(self):
        """Perform a full game restart and begin play.

        This resets dynamic settings and game statistics, recenters the ship,
        clears bullets and aliens, recreates the fleet, and sets the game
        to active so the main loop begins updating objects.
        """
        self.settings.initialize_dynamic_settings() # Reset dynamic settings (speeds, counts)
        self.game_stat = GameStat(self)             # Reset game stats (ships left, etc.)
        self.HUD.update_scores()                    # Update HUD to reflect reset stats

        self.ship._center_ship()                    # Reset ship position
        self.ship.arsenal.arsenal.empty()           # Clear ship's bullets

        self.alien_fleet.fleet.empty()              # Clear existing aliens
        self.alien_fleet.create_fleet()             # Create a new alien fleet

        self.game_active = True                     # Start the game
        pygame.mouse.set_visible(False)             # Hide mouse cursor during play



    def _update_screen(self):
        """Draw the background, ship, fleet and flip the display."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()


        #draw HUD
        self.HUD.draw()


        # Draw the play button when the game is not active
        if not self.game_active:
            self.play_button.draw()
        pygame.display.flip()

    def _check_events(self):
        """Process pygame events and dispatch to handlers."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(event)
    
    def _check_keyup_events(self, event):
        """Handle key release events to stop continuous actions.

        Args:
            event (pygame.event.Event): KEYUP event instance.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_keydown_events(self, event):
        """Handle key press events for movement, firing, and quitting.

        Args:
            event (pygame.event.Event): KEYDOWN event instance.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:

            if self.ship.fire():
              self.laser_sound.play()
              self.laser_sound.fadeout(250)

            #play the laser sound
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()
    
    def _check_play_button(self, event):
        """Check if the play button was clicked.
        
        Args:
            event (pygame.event.Event): MOUSEBUTTONDOWN event instance.
        """
        mouse_pos = pygame.mouse.get_pos()
        if not self.game_active and self.play_button.check_clicked(mouse_pos):
            # Start a fresh game (reset stats, ship, bullets, and fleet)
            self.restart_game()
 

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()