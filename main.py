import oz_engine as oz
import time
import os
import random

cell_pos_list = set()
cell_to_remove = set()
cell_to_born = set()

evaluated_dead_cell = set()


class Cell(oz.Sprite):

    __slots__ = "canvas_owner", "position", "name", "group"

    def __init__(self, canvas_owner, position : dict, name : str, group=None):

        self.register_info(canvas_owner, "█", position, name , group)
        cell_pos_list.add((self.position["x"], self.position["y"]))



    def get_number_of_neighboor(self, position : dict):
        #give the amount of neighboor

        Tiles_to_check = [
            (-1, -1), (0, -1), (1,  -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0)
        ]

        neighboor_count = 0


        for tile in Tiles_to_check:

            current_pos = (tile[0] + position["x"], tile[1] + position["y"])
            if current_pos in cell_pos_list:

                neighboor_count += 1

        return neighboor_count


    def check_if_dies(self, neighboor_count : int):

        if not neighboor_count == 2 or  neighboor_count == 3:
            cell_to_remove.add(self)


        elif camera.is_renderable(self.position) == False:
            cell_to_remove.add(self)


    def check_if_reproduction(self):



        Tiles_to_check = [
            (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0)
        ]


        for tile in Tiles_to_check:

            current_pos = (tile[0] + self.position["x"],  tile[1] + self.position["y"])

            if current_pos not in cell_pos_list:

                evaluated_dead_cell.add(current_pos)

                Tiles_to_check_child = [
                    (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1),
                    (0, 1), (-1, 1), (-1, 0)
                ]

                for tile_child in Tiles_to_check_child:

                    current_pos_child = (current_pos[0] + tile_child[0], current_pos[1] + tile_child[1])
                    neighboor_reproduction_count_check = self.get_number_of_neighboor({"x" : current_pos_child[0], "y" : current_pos_child[1]})


                    if neighboor_reproduction_count_check == 3:

                        cell_to_born.add((current_pos_child[0], current_pos_child[1]))


def born_cell_at(x : int, y : int):
    cell1 = Cell(canvas, {"x": x, "y": y}, "cell")


def born_gosper_canon_at(x : int , y : int):
    born_cell_at(0 + x, 0 + y)
    born_cell_at(1 + x, 0 + y)
    born_cell_at(0 + x, 1+ y)
    born_cell_at(1 + x, 1+ y)

    born_cell_at(10 + x, 0+ y)
    born_cell_at(10 + x, 1+ y)
    born_cell_at(10 + x, 2+ y)
    born_cell_at(11 + x, 3+ y)
    born_cell_at(12 + x, 4+ y)
    born_cell_at(13 + x, 4+ y)
    born_cell_at(11 + x, -1+ y)
    born_cell_at(12 + x, -2+ y)
    born_cell_at(13 + x, -2+ y)

    # petit carré
    born_cell_at(14 + x, 1+ y)

    born_cell_at(15 + x, -1+ y)
    born_cell_at(16 + x, 0+ y)
    born_cell_at(16 + x, 1+ y)
    born_cell_at(17 + x, 1+ y)
    born_cell_at(16 + x, 2+ y)
    born_cell_at(15 + x, 3+ y)

    born_cell_at(22 + x, 1+ y)
    born_cell_at(20 + x, 0+ y)
    born_cell_at(20 + x, -1+ y)
    born_cell_at(20 + x, -2+ y)
    born_cell_at(21 + x, 0+ y)
    born_cell_at(21 + x, -1+ y)
    born_cell_at(21 + x, -2+ y)
    born_cell_at(22 + x, -3 + y)

    born_cell_at(24 + x, -3 + y)
    born_cell_at(24 + x, -4 + y)

    born_cell_at(24 + x, 1 + y)
    born_cell_at(24 + x, 2 + y)

    born_cell_at(34 + x, -2 + y)
    born_cell_at(35 + x, -2 + y)
    born_cell_at(34 + x, -1 + y)
    born_cell_at(35 + x, -1 + y)


def choose_config():

    action = int(input("Give canvas size: -x:"))
    camera.size["x"] = action
    action = int(input("Give canvas size: -y:"))
    camera.size["y"] = action

    action = input("What you like to start with:\n1-Random Configuration\n2-Gosper Glider Gun\n")
    if action == "1":
        action = int(input("give a spawn ratio 1 on *YOUR NUMBER* that a cell will be alive:"))
        INT_RANGE = action

        for y in range(0 , camera.size["y"]):
            for x in range(0, camera.size["x"]):

                if random.randint(1, INT_RANGE) == 1:
                    born_cell_at(x, y)

        game()

    elif action == "2":

        add_new_canon = True
        while add_new_canon:
            x = int(input("set x: "))
            y = int(input("set y: "))
            born_gosper_canon_at(x, y)
            action = input("would you like to add another one (y/n) : ")
            add_new_canon = True if action == "y" else False

        game()

def game():
    global cell_pos_list
    global cell_to_remove
    global cell_to_born
    

    print(camera.render())

    while True:



        ### CALCULATE ###
        for cell in canvas.sprite_tree:

            neighboor_count = cell.get_number_of_neighboor(cell.position)
            cell.check_if_reproduction()
            cell.check_if_dies(neighboor_count)
        ###

        evaluated_dead_cell = set()


        ### KILL ###
        for dead_cell in cell_to_remove.copy():

            pos = (dead_cell.position["x"], dead_cell.position["y"])
            if pos in cell_pos_list:
                cell_pos_list.remove(pos)
            dead_cell.kill()

        cell_to_remove = set()
        ###

        ### BORN ###
        for new_cell in cell_to_born:
            born_cell_at(new_cell[0], new_cell[1])
        cell_to_born = set()
        ###

        os.system("cls")
        print(camera.render())
        time.sleep(0.1)


canvas = oz.Canvas(" ")
camera = oz.Camera(canvas, {"x" : 100, "y" : 50}, {"x" : 0 ,"y" : 0}, "camera")

choose_config()







