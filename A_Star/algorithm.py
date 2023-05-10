from queue import PriorityQueue

class Algorithm:
    """A class that contains the A* algorithm"""
    def h(p1: tuple, p2: tuple) -> int:
        """Returns the Manhattan distance between two points"""
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def neighbors(maze: list, current: tuple) -> list(tuple()):
        """Returns the neighbors of the current node"""
        x, y = current
        neighbors = []

        if x > 0 and maze[y][x - 1] == 0: # UP
            neighbors.append((x - 1, y))
        if x < len(maze[0]) - 1 and maze[y][x + 1] == 0: # DOWN
            neighbors.append((x + 1, y))
        if y > 0 and maze[y - 1][x] == 0: # LEFT
            neighbors.append((x, y - 1))
        if y < len(maze) - 1 and maze[y + 1][x] == 0: # RIGHT
            neighbors.append((x, y + 1))

        if x > 0 and y > 0 and maze[y - 1][x - 1] == 0: # UP-left
            neighbors.append((x - 1, y - 1))
        if x > 0 and y < len(maze) - 1 and maze[y + 1][x - 1] == 0: # UP-right
            neighbors.append((x - 1, y + 1))
        if x < len(maze[0]) - 1 and y > 0 and maze[y - 1][x + 1] == 0: # DOWN-left
            neighbors.append((x + 1, y - 1))
        if x < len(maze[0]) - 1 and y < len(maze) - 1 and maze[y + 1][x + 1] == 0: # DOWN-right
            neighbors.append((x + 1, y + 1))

        for neighbor in neighbors:
            yield neighbor

    def spots(maze: list) -> tuple():
        """Returns a list of all the spots in the maze"""
        for i, row in enumerate(maze):
            for j, spot in enumerate(row):
                yield (j, i)

    def path(came_from: dict, current: tuple) -> tuple():
        """Draws the path from the start to the end"""
        while current in came_from:
            current = came_from[current]
            yield current
    
    def astar(maze, start: tuple, end: tuple) -> tuple() or None:
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""
        
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from: dict = {}

        g_score = {spot: float("inf") for spot in Algorithm.spots(maze)}
        g_score[start] = 0
        f_score = {spot: float("inf") for spot in Algorithm.spots(maze)}
        f_score[start] = Algorithm.h(start, end)

        open_set_hash = {start}

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                yield (came_from, end)
            
            for neighbor in Algorithm.neighbors(maze, current):
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + Algorithm.h(neighbor, end)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        yield (neighbor, "open")

            if current != start:
                yield (current, "closed")

        return None
            
            


if __name__ == '__main__':
    print("This is a module, not a script. Please run game.py instead.")