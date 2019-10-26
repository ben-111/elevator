# elevator.py
#
# Programmer : Ben L.
# Date       : 18/10/2019
#
#
# This is an elevator.
#--------------------------------------------------------------

# Set version
__version__ = '1.0.0'

# Imports
import time

# Constants
FLOOR = 0
DIRECTION = 1

class elevator:
    def __init__(self, floors=3, starting_floor=0):
        """Create new elevator object."""
        self._floors = floors
        self._calls = {}
        self.IDLE = None
        self.UP = 1
        self.DOWN = -1
        self._current_state = [starting_floor, self.IDLE]
        self.opened = 0

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self, floors):
        if floors < 2:
            raise ValueError("The elevator needs at least two floors to operate")
        self._floors = floors

    def call_floor(self, floor, direction=None):
        if floor > self._floors or floor < 0:
            raise ValueError("No such floor")
        
        if direction not in (self.IDLE, self.UP, self.DOWN):
            raise ValueError("No such direction")
        
        if floor == 0 and direction == self.DOWN:
            raise ValueError("Can't go down here")
        
        if floor == self._floors and direction == self.UP:
            raise ValueError("Can't go up here")
        
        if direction and floor not in self._calls.keys(): # Won't override direction
            self._calls[floor] = direction
            
        elif direction is None: # Unless direction is None
            self._calls[floor] = None

    def advance(self):

        # Current state
        current_floor = self._current_state[FLOOR]
        current_direction = self._current_state[DIRECTION]

        def opposite_direction(direction):
            if direction == self.UP:
                return self.DOWN
            if direction == self.DOWN:
                return self.UP

        # Filter functions
        above = {floor: self._calls[floor] for floor in self._calls.keys()\
                 if floor > current_floor}
        below = {floor: self._calls[floor] for floor in self._calls.keys()\
                 if floor < current_floor}
        up_calls = lambda x: x == self.UP
        down_calls = lambda x: x == self.DOWN
        
        # Elevator functions
        def open_doors():
            """Opens door and removes call"""
            print("~~~Opening doors~~~")

            # Open door
            self.opened += 1

            # For extra realism you can uncomment:
            # time.sleep(5)

            # Removes call from current floor
            self._calls.pop(current_floor)

        def go_up():
            """Goes up one floor"""
            if self._current_state[FLOOR] < self._floors:
                self._current_state[FLOOR] += 1
                print(f"...{self._current_state[FLOOR]}")
            else:
                raise Exception("Can't go further up")

        def go_down():
            """Goes down one floor"""
            if self._current_state[FLOOR] > 0:
                self._current_state[FLOOR] -= 1
                print(f"...{self._current_state[FLOOR]}")
            else:
                raise Exception("Can't go further down")

        def start_going_up():
            """Changes current direction to up"""
            self._current_state[DIRECTION] = self.UP

        def start_going_down():
            """Changes current direction to down"""
            self._current_state[DIRECTION] = self.DOWN

        def switch_direction():
            """Switches current direction from up to down or from down to up"""
            if current_direction == self.DOWN:
                start_going_up()
            elif current_direction == self.UP:
                start_going_down()

        def rest():
            """"Switches current direction to idle"""
            self._current_state[DIRECTION] = self.IDLE

        # Logic:
        # If elevator is moving (not idle)
        if current_direction:

            # If there's a call in the current floor
            if current_floor in self._calls.keys():

                # If the call is in the opposite direction
                if self._calls[current_floor] == opposite_direction(current_direction):

                    # If the current direction is up
                    if current_direction == self.UP:

                        # If there are calls above
                        if above:
                            go_up()

                        # If there aren't calls above
                        else:
                            open_doors()
                            switch_direction()
                    
                    # If the current direction is down 
                    else:

                        # If there are calls below
                        if below:
                            go_down()

                        # If there aren't calls below
                        else:
                            open_doors()
                            switch_direction()

                # If the call isn't in the opposite direction (either same or None)
                else:
                    open_doors()

            # If there isn't a call in the current floor
            else:

                # If the current direction is up
                if current_direction == self.UP:

                    # If there are calls above
                    if above:
                        go_up()

                    # If there aren't calls above
                    else:

                        # If there are calls below
                        if below:
                            switch_direction()

                        # If there aren't calls below
                        else:
                            rest()

                # If the current direction is down
                else:

                    # If there are calls below
                    if below:
                        go_down()

                    # If there aren't calls below
                    else:

                        # If there are calls above
                        if above:
                            switch_direction()

                        # If there aren't calls above
                        else:
                            rest()

        # If elevator is idle
        else:

            # If there's a call in the current floor
            if current_floor in self._calls.keys():
                open_doors()

            # If there isn't a call in the current floor
            else:

                # If there are up-calls below
                if list(filter(up_calls, below.values())):
                    start_going_down()

                # If there are down-calls above
                elif list(filter(down_calls, above.values())):
                    start_going_up()

                # If there are calls above
                elif above:
                    start_going_up()

                # If there are calls below
                elif below:
                    start_going_down()

    def advance_until_stop(self):
        """Advances until the elevator opens its doors"""
        if self._calls:
            self.opened = 0
            while not self.opened:
                self.advance()

    def advance_until_floor(self, floor):
        """Advances until elevator reaches floor"""
        if self._calls:
            while not self._current_state[FLOOR] == floor:
                self.advance()
                

def main():
    # Define new elevator object with 5 floors
    new_elevator = elevator(5)
    up = new_elevator.UP
    down = new_elevator.DOWN
    new_elevator.call_floor(0, up)
    new_elevator.advance()
    new_elevator.call_floor(3)
    new_elevator.advance_until_floor(2)
    new_elevator.call_floor(1, down)
    new_elevator.call_floor(5, down)
    new_elevator.advance_until_stop()
    new_elevator.advance_until_stop()
    new_elevator.advance_until_stop()
    
    

if __name__ == '__main__':
    main()
