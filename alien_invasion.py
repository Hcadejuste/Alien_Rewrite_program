import sys
import pygame
from setting import Settings
from game_stat import GameStat
from ship import Ship
from arsenal import Arsenal
from alien import Alien
from alien_fleet_file import AlienFleet
from time import sleep



class AlienInvasion:
    """Main class that manages the game assets and behavior.""" 
    def __init__(self):
        """Prepare the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        # track game status (ships left, active state, etc.)
        self.game_stat = GameStat(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))

        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
                                         (self.settings.screen_w, self.settings.screen_h)
            )

    


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
        self.game_active = True

        


        

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self._check_events() 
            if self.game_active:
                self.alien_fleet.update_fleet()
                self.ship.update()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.FPS)



    
    def _check_collisions(self):
        # check collisins for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self.check_games_status()


        # check collisions for aliens and bottom of the screen
        if self.alien_fleet.check_fleet_bottom():
            # call the handler to update ships/level when fleet reaches bottom
            self.check_games_status()





        # check collision of alien and projectiles. 

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact.play()
            self.impact.fadeout(500)

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()    


           
    def check_games_status(self):
        # decrement remaining ships and reset level, or end game
        if self.game_stat.ship_limit > 0:
            self.game_stat.ship_limit -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _update_screen(self):
        """Update images on the screen, and flips to the new screen."""
        self.screen.blit(self.bg, (0, 0)) 
        self.ship.draw()  
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self):
        """React to keypresses and mouse events."""  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
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
            
        
       

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()