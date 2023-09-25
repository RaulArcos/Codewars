# The Lift (3kyu) - https://www.codewars.com/kata/58905bfa1decb981da00009e
# @autor: Raul Arcos Herrera

from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = -1

class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.queues = []
        self.queues.extend(list(queue) for queue in queues)
        self.capacity = capacity
        self.trace = [0]
        print (self.queues)
        self.direction = Direction.UP
        self.currentLoad = []
        pass
        
    def theLift(self):
        while not self.lift_job_completed():
            self.people_movement()
            print (self.queues)
            print (self.trace[-1], self.currentLoad, self.direction)
            next_floor = self.next_floor()
            if next_floor != self.trace[-1]:
                self.trace.append(next_floor)
            self.update_direction()
        return self.trace
    
    def lift_job_completed(self):
        return all(not queue for queue in self.queues) and not len(self.currentLoad)
    
    def people_movement(self):
        indices_to_remove = []
        self.currentLoad = [person for person in self.currentLoad if person != self.trace[-1]]
        currentLoad = len(self.currentLoad)
        if self.direction == Direction.UP:
            for index, person in enumerate(self.queues[self.trace[-1]]):
                if person > self.trace[-1] and currentLoad < self.capacity:
                    indices_to_remove.append(index)
                    currentLoad+=1
        else:
            for index, person in enumerate(self.queues[self.trace[-1]]):
                if person < self.trace[-1] and currentLoad < self.capacity:
                    indices_to_remove.append(index)
                    currentLoad+=1

        for index in reversed(indices_to_remove):
            self.currentLoad.append(self.queues[self.trace[-1]].pop(index))
            
    def update_direction(self):
        if self.trace[-1] == len(self.queues)-1:
            self.direction = Direction.DOWN
            return
        elif self.trace[-1] == 0:
            self.direction = Direction.UP
            return
        elif self.direction == Direction.UP:
            for person in self.currentLoad:
                if person > self.trace[-1]:
                    return
            for x in range(self.trace[-1]+1, len(self.queues), self.direction.value):
                if len(self.queues[x]):
                    return
            for person in self.queues[self.trace[-1]]:
                if person > self.trace[-1]:
                    return
            self.direction = Direction.DOWN
            return
        elif self.direction == Direction.DOWN:
            for person in self.currentLoad:
                if person < self.trace[-1]:
                    return
            for x in range(self.trace[-1]-1, -1, self.direction.value):
                if len(self.queues[x]):
                    return
            for person in self.queues[self.trace[-1]]:
                if person < self.trace[-1]:
                    return
            self.direction = Direction.UP
    
    def closest_floor_with_people(self, currentFloor):
        closest = 0
        distance = 99
        for floor in range(-1, len(self.queues)):
            if len(self.queues[floor]) and floor != currentFloor:
                if distance > abs(floor-currentFloor):
                    closest = floor
                    distance = abs(floor-currentFloor)
        return closest
    
    def closest_floor_to_people_in_elevator(self, currentFloor):
        if self.direction == Direction.UP:
            posible_floors = [person for person in self.currentLoad if person > self.trace[-1]]
        else:
            posible_floors = [person for person in self.currentLoad if person < self.trace[-1]]
        closest = 0
        distance = 99
        for floor in posible_floors:
            if distance > abs(floor-currentFloor):
                closest = floor
                distance = abs(floor-currentFloor)
        return closest
    
    def next_floor(self):
        next_floor = 0
        if len(self.currentLoad):
            next_floor = self.closest_floor_to_people_in_elevator(self.trace[-1])
            if self.direction == Direction.UP:
                for floor in range(self.trace[-1]+1, next_floor, self.direction.value):
                    if len(self.queues[floor]) and any(person > floor for person in self.queues[floor]):
                        return floor
            else: 
                for floor in range(self.trace[-1]-1, next_floor, self.direction.value):
                    if len(self.queues[floor]) and any(person < floor for person in self.queues[floor]):
                        return floor
        else:
            next_floor = self.closest_floor_with_people(self.trace[-1])
            if self.direction == Direction.UP:
                for floor in range(self.trace[-1], len(self.queues), self.direction.value):
                    if len(self.queues[floor]) and any(person < floor for person in self.queues[floor]):
                        next_floor = floor
                for floor in range(self.trace[-1], next_floor, self.direction.value):
                    if len(self.queues[floor]) and any(person > floor for person in self.queues[floor]):
                        return floor
            else:
                for floor in range(self.trace[-1], -1, self.direction.value):
                    if len(self.queues[floor]) and any(person > floor for person in self.queues[floor]):
                        next_floor = floor
                for floor in range(self.trace[-1], next_floor, self.direction.value):
                    if len(self.queues[floor]) and any(person < floor for person in self.queues[floor]):
                        return floor
                    
            if self.trace[-1] == 0:
                 for floor in range(self.trace[-1], len(self.queues), self.direction.value):
                    if len(self.queues[floor]) and any(person > floor for person in self.queues[floor]):
                        return floor
        return next_floor