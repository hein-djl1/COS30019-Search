import sys
from node import SearchNode

def iddfs(graph):
    """Iterative Deepening DFS"""
    total_nodes = 0
    start = graph.origin
    
    for limit in range(sys.maxsize):
        start_node = SearchNode(start, None, None, 0)
        total_nodes += 1
        
        stack = [(start_node, 0, {start.id})]
        cutoff_occurred = False
        goal_node = None
        
        while stack:
            current, depth, current_path = stack.pop()
            
            if graph.is_goal(current.state):
                goal_node = current
                break
                
            if depth == limit:
                cutoff_occurred = True
                continue
                
            neighbours = graph.get_neighbours(current.state.id)
            for neighbour, cost in reversed(neighbours):
                if neighbour.id not in current_path:
                    child = SearchNode(neighbour, current, cost, current.path_cost + cost)
                    total_nodes += 1
                    
                    new_path = current_path.copy()
                    new_path.add(neighbour.id)
                    stack.append((child, depth + 1, new_path))
                    
        if goal_node:
            return goal_node.state.id, total_nodes, goal_node.get_path()
        if not cutoff_occurred:
            return None, total_nodes, [] # Search space exhausted
            
    return None, total_nodes, []