from pathlib import Path

class Settings:
    """ a class to store all settings for Alien Invasion"""
    def __init__(self):
        """Prepare the game's settings."""
        self.name: str = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        #frames per second
        self.FPS = 60
        
        self.bg_file = Path.cwd() / 'image' / 'bakground_image.png'
    

        self.ship_file = Path.cwd()  / 'image' / 'ship.bmp'
        self.ship_w = 70      
        self.ship_h = 95     


        self.difficulty_scale = 1.5

        self.bullet_file = Path.cwd()/ 'image' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'sound' / 'laser.mp3'
        self.impact = Path.cwd() / 'sound' / 'impactSound.mp3'
        
        
        self.alien_file = Path.cwd() /'image' / 'alien.bmp' 
       
        self.alien_w  = 40 
        self.alien_h = 40
        self.fleet_direction = 1 
        
        # Button settings
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 50)
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.font_file = Path.cwd() / 'Roboto' / 'Roboto-Italic-VariableFont_wdth,wght.ttf'

    def initialize_dynamic_settings(self):
        
        self.ship_speed = 5
        self.starting_ship_count = 3
        self.bullet_speed = 7
        self.bullet_amount = 5
        self.fleet_speed = 2  
        self.fleet_drop_speed = 40
        self.bullet_w = 25
        self.bullet_h = 80

    def increase_difficulty(self):
        self.ship_speed *= self.difficulty_scale    
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale