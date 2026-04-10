from node import SearchNode
from node import SearchNode
from heuristic import nearest_goal_dist

def idastar(graph):
    """Iterative Deepening A*"""
    total_nodes = 0
    start = graph.origin
    goals = graph.destinations

    # initialize the threshold to the heuristic value of the start node
    threshold = nearest_goal_dist(start, goals)
    
    while True:
        #________________Debugging lines_________________
        print(f"\n--- Starting Pass with Threshold: {threshold:.2f} ---")
        #________________Debugging lines_________________
        #origin node
        start_node = SearchNode(start, None, None, 0)
        total_nodes += 1
        
        #add start_node to frontier (stack) with its path (just itself at the start)
        stack = [(start_node, {start.id})]
        # track the minimum f value that exceeded the current threshold, to use as the next threshold
        # set to infinity, update it whenever we can find an f that exceeds the threshold
        min_exceeded_cost = float('inf')
        goal_node = None
        
        while stack:
            current, current_path = stack.pop()
            
            #update f value for current node
            g = current.path_cost
            h = nearest_goal_dist(current.state, goals)
            f = g + h

            #________________Debugging lines_________________
            if f > threshold:
                print(f"  CUTOFF: Node {current.state.id} | f={f:.2f} (Threshold: {threshold:.2f})")
                min_exceeded_cost = min(min_exceeded_cost, f)
                continue
            
            print(f"  Expanding: Node {current.state.id} | g={g}, h={h:.2f}, f={f:.2f}")
            #________________Debugging lines_________________
            
            if f > threshold:
                min_exceeded_cost = min(min_exceeded_cost, f)
                continue
                
            #goal test
            if graph.is_goal(current.state):
                goal_node = current
                break
            
            #expand node
            neighbours = graph.get_neighbours(current.state.id)
            for neighbour, cost in reversed(neighbours):
                #check if it is already in the current path to avoid cycles
                if neighbour.id not in current_path:
                    child = SearchNode(neighbour, current, cost, current.path_cost + cost)
                    total_nodes += 1
                    # create a new path set for the child node, which is the current path plus the new neighbour
                    new_path = current_path.copy()
                    new_path.add(neighbour.id)
                    stack.append((child, new_path))
                    
        if goal_node:
            return goal_node.state.id, total_nodes, goal_node.get_path()
        if min_exceeded_cost == float('inf'):
            return None, total_nodes, [] # Search space exhausted
            
        threshold = min_exceeded_cost