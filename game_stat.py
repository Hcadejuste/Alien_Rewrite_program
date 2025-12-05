from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  
    from alien_invasion import AlienInvasion


class GameStat():
    def __init__(self, game: 'AlienInvasion'):
        self.game = game 
        self.settings = game.settings
        self.init_saved_scores()
        self.max_score = 0
        self.reset_stats()


    def init_saved_scores(self):
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat().st_size>0:#self.path.stat.__sizeof__() > 80:
            contents  = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else: 
            self.hi_score = 0
            # Save the file
            self.save_scores()


    def save_scores(self): 
        scores = {
            'hi_score': self.hi_score
        }  
        contents = json.dumps(scores, indent = 4)
        try:
           self.path.write_text(contents)   

        except FileNotFoundError as e: 
            print("There is no such file, sorry")     


    def reset_stats(self):
        self.ship_limit = self.settings.starting_ship_count
        self.score = 0 
        self.level = 1

    def update(self, collisions):
        # update score
        if self.score > self.max_score:
         self.max_score = self.score

        self._update_score(collisions)

        # update max_score 
        self._update_max_score()


        # update hi_score
        self._update_hi_score()





    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score =  self.score
           


    def _update_score(self, collisions):
        for alien in collisions.values():
            self.score += self.settings.alien_points
            print(self.score)

    def _update_hi_score(self):
        if self.score > self.hi_score:
            self.hi_score =  self.score        


 


    def update_level(self):
        self.level += 1      




           





        