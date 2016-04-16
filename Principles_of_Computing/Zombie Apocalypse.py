"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = [[EMPTY for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        boundry = poc_queue.Queue()
        method = self.zombies if (entity_type == ZOMBIE) else self.humans
        for item in method():
            boundry.enqueue(item)
            visited[item[0]][item[1]] = FULL
            distance_field[item[0]][item[1]] = 0
        while (len(boundry) > 0):
            now = boundry.dequeue()
            for cell in self.four_neighbors(now[0], now[1]):
                if ((visited[cell[0]][cell[1]] == EMPTY) and (self.is_empty(cell[0], cell[1]))):
                    visited[cell[0]][cell[1]] = FULL
                    boundry.enqueue(cell)
                    distance_field[cell[0]][cell[1]] = distance_field[now[0]][now[1]] + 1
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index in range(len(self._human_list)):
            human = self._human_list[index]
            max_distance = zombie_distance[human[0]][human[1]]
            choices = [human]
            for destination in self.eight_neighbors(human[0], human[1]):
                if (self.is_empty(destination[0], destination[1])):
                    if (zombie_distance[destination[0]][destination[1]] > max_distance):
                        max_distance = zombie_distance[destination[0]][destination[1]]
                        choices = [destination]
                    elif (zombie_distance[destination[0]][destination[1]] == max_distance):
                        choices.append(destination)
            self._human_list[index] = random.choice(choices)
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #distance_field = self.compute_distance_field(HUMAN)
        for index in range(len(self._zombie_list)):
            zombie = self._zombie_list[index]
            min_distance = human_distance[zombie[0]][zombie[1]]
            choices = [zombie]
            for destination in self.four_neighbors(zombie[0], zombie[1]):
                if (self.is_empty(destination[0], destination[1])):
                    if (human_distance[destination[0]][destination[1]] < min_distance):
                        min_distance = human_distance[destination[0]][destination[1]]
                        choices = [destination]
                    elif (human_distance[destination[0]][destination[1]] == min_distance):
                        choices.append(destination)
            self._zombie_list[index] = random.choice(choices)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Zombie(30, 40))
