import pygame

class Grid():
    def __init__(self, game):
        self.game = game
        self.grid_size = (10, 20)
        self.grid = {}
        self.base_color = (10,10,10)
        #Holds all the active grid points, so that they wont disappear 
        self.active_spaces = []

        #sets up the grid and its associated values
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                grid_key = str(x) + ',' + str(y)
                self.grid[grid_key] = {'pos': (x,y), 'active': 0, 'color': self.base_color, 'in_use': False}

    def render(self):
        self.update()
        if self.game.active_object:
            cur_object = self.game.active_object
            x_mod = 0
            y_mod = 0
            for i in range(len(cur_object['shape'])):
                if cur_object['shape'][i] < 0:
                    x_mod = 0
                    y_mod += 1
                    continue
                elif cur_object['shape'][i] > 0:
                    x_val = int(cur_object['location'][0]) + x_mod
                    y_val = int(cur_object['location'][1]) + y_mod
                    coordinates = str(x_val) + ',' + str(y_val)
                    self.grid[coordinates]['color'] = cur_object['color'][1]
                    self.grid[coordinates]['active'] = 1
                    self.grid[coordinates]['in_use'] = True
                    #This is the problem
                x_mod += 1
                

        for key in self.grid:
            if self.grid[key]['active'] <= 0:
                color = self.base_color
            else:
                if self.grid[key] in self.active_spaces:
                    print('Its here!')
                    color = (255,0,255)
                color = self.grid[key]['color']
            loc = self.grid[key]['pos']
            rect = pygame.Rect(loc[0], loc[1], 1, 1)

            pygame.draw.rect(self.game.tetris_display, color, rect)

    def update(self):
        for key, value in self.grid.items():
            if key in self.active_spaces:
                value['active'] = 1
            else:
                value['active'] = 0
            
    
    def set_piece(self, object):
        object = self.game.active_object
        x_mod = 0
        y_mod = 0
        for i in range(len(object['shape'])):
            if object['shape'][i] < 0:
                x_mod = 0
                y_mod += 1
                continue
            elif object['shape'][i] > 0:
                x_val = int(object['location'][0]) + x_mod
                y_val = int(object['location'][1]) + y_mod
                coordinates = str(x_val) + ',' + str(y_val)
                self.grid[coordinates]['color'] = object['color'][1]
                self.grid[coordinates]['active'] = 1
                self.grid[coordinates]['in_use'] = False
                self.active_spaces.append(str(x_val) + ',' + str(y_val))
            x_mod += 1

    #Clears any location in the grid and removes it from the active spaces
    def clear_pixel(self, coordinate:str):
        location = self.grid[coordinate]
        location['active'] = 0
        location['in_use'] = False
        #print(self.active_spaces, location['pos'])
        for x in range(0, len(self.active_spaces)):
            print(coordinate == self.active_spaces[x])
            if coordinate == self.active_spaces[x]:
                print(coordinate, self.active_spaces)
                self.active_spaces.pop(x)
                return

    #This clears the entire xlevel at any given y level
    def clear_line(self, y_level):
        for x in range(self.grid_size[0]):
            coords = str(x) + ',' + str(y_level)
            self.clear_pixel(coords)
            print('Cleared coords ' + coords)
        

    def clear_grid(self):
        for key, value in self.grid.items():
            #value['color'] = self.base_color
            value['active'] = 0
            value['in_use'] = False
            self.active_spaces.clear()
