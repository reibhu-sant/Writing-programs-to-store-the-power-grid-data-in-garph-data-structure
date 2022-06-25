import csv


class House:
    def __init__(self, number, power):
        self.house_no = number
        self.power_required = power
        self.assigned_propagator_no = -1

    def assign_propagtor(self, number):
        self.assigned_propagator_no = number

    def __str__(self):
        return f"house_no: {self.house_no} power_required: {self.power_required}"


class Propagator:
    def __init__(self, number, max_power):
        self.propagator_no = number
        self.maximum_power = max_power
        self.power_remaining = max_power
        self.houses_connected = list()

    def __str__(self):
        return f"no : {self.propagator_no} max_power: {self.maximum_power} power_remaining: {self.power_remaining}"

    def connected_houses_info(self):
        for house in self.houses_connected:
            print(house)

    # check if the house is connected part of the list or not.           
    def is_house_present(self, house_no):
        flag = False
        for i in range(len(self.houses_connected)):
            if house_no == self.houses_connected[i].house_no:
                flag = True
                break
        if flag:
            return i
        else:
            return -1

    # Add the house in the list.
    # Before adding check if the house is already connected
    def add_house(self, house: House):
        if self.is_house_present(house.house_no) == -1:
            if self.power_remaining >= house.power_required:
                self.power_remaining = self.power_remaining - house.power_required
                self.houses_connected.append(house)
                return True
            else:
                return False
        else:
            return False

    # Remove the house from the list, before removing need to check
    # if the house is in the assigned propagator list.
    def remove_house(self, house_no: int):
        if self.is_house_present(house_no) != -1:
            rem_house = self.houses_connected[self.is_house_present(house_no)]
            self.power_remaining = self.power_remaining + rem_house.power_required
            self.houses_connected.remove(rem_house)
            return True
        else:
            return False


class PowerGrid:
    def __init__(self):
        self.propagators = dict()

    # Adding the propagtor into in the dictionary. 
    # Check if the propagator is not part of the dictioary already
    # It will not posess any value in the beginning. 
    def add_propagator(self, propagator: Propagator):
        count = 0
        for node in self.propagators.keys():
            if node == propagator.propagator_no:
                count = 1
        if count == 1:
            return False
        elif count == 0:
            self.propagators[propagator.propagator_no] = propagator
            return True

    # Removing the propagtor into in the dictionary. 
    # Check if the propagator is part of the dictioary or not    
    def remove_propagator(self, propagator_no):
        count = 0
        for key, val in list(self.propagators.items()):
            if key == propagator_no:
                self.propagators.pop(propagator_no)
                count = count + 1
        if count == 1:
            return True
        elif count == 0:
            return False

    def add_house(self, house: House, propagator_no: int):
        if propagator_no in self.propagators:
            return self.propagators[propagator_no].add_house(house)
        else:
            return False

    def remove_house(self, house_no: int, propagator_no: int):
        if propagator_no in self.propagators:
            return self.propagators[propagator_no].remove_house(house_no)
        else:
            return False


def create_power_grid():
    power_grid = PowerGrid()

    with open('app.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            entity_type = row['Type']

            if entity_type == "propagator":
                propagator = Propagator(int(row['Entity_Number']), int(row['Power']))
                power_grid.add_propagator(propagator)

            elif entity_type == "house":

                house = House(int(row['Entity_Number']), int(row['Power']))
                house.assigned_propagator_no = int(row['Assigned_Propagator'])

                power_grid.add_house(house, int(row['Assigned_Propagator']))

    return power_grid


if __name__ == "__main__":
    power_grid = create_power_grid()

    for _, propagator in power_grid.propagators.items():
        # Printing the propagator information
        print(f"Propagator No : {propagator.propagator_no}")
        print("------------Propagator Information-----------------")
        print(propagator)
        print("------------Connected Houses Information-----------------")
        propagator.connected_houses_info()
        print("\n")

    print("----Removing House 1014 from Propagator 1002----")
    if power_grid.remove_house(1014, 1002):
        print("House 1014 is successfully removed from Propagator 1002")
    else:
        print("House 1014 is not connected with Propagator 1002")

    print("\n----Removing House 1024 from Propagator 1003----")
    if power_grid.remove_house(1024, 1003):
        print("House 1024 is successfully removed from Propagator 1003")
    else:
        print("House 1024 is not connected with Propagator 1003")


