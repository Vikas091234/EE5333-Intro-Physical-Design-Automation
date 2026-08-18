"""
Course      : EE5333 - Introduction to Physical Design Automation
Assignment  : 2
Program     : Fiduccia-Mattheyses Hypergraph Partitioning

Description :
Implements the Fiduccia-Mattheyses algorithm to
bi-partition a hypergraph while satisfying area
constraints and minimizing the number of cut hyperedges.

Author      : Vikas Raj
"""

# bi-partition the input hypergraph using Fiduccia-Matheyses algorithm
# argument list is the same as the ILP version described above
# return value is a list of two lists and the number of cut hyperedges;
# each list is a partition comprising contained gates(vertices)
import random

def partitionFM(V, E, Amin, Amax):

    # --- Initialization ---
    nodes = list(V.keys())
    partition = {} 
    
    # Create an initial random but balanced partition
    random.shuffle(nodes)
    area0 = 0
    area1 = 0

    for node in nodes:
        node_area = V[node]._area # Access numerical area from Vertex object
        if area0 + node_area <= Amax:
            partition[node] = 0
            area0 += node_area
        else:
            partition[node] = 1
            area1 += node_area
    # Verify that the initial partition satisfies the area constraints
    if not (Amin <= area0 <= Amax and Amin <= area1 <= Amax):
        raise ValueError("Unable to create a feasible initial partition")

    def get_cut_cost(current_partition):
        """Calculates the number of nets spanning across both partitions."""
        cuts = 0
        for net, gates in E.items():
            # Check if vertices in the net belong to more than one partition
            parts = set(current_partition[g._name] for g in gates if g._name in current_partition)
            if len(parts) > 1:
                cuts += 1
        return cuts

    def calculate_gain(node, current_partition):
        """Calculates the reduction in cut-sets if 'node' is moved to the other side."""
        gain = 0
        from_part = current_partition[node]
        to_part = 1 - from_part

        for net, gates in E.items():
            gate_names = [g._name for g in gates]
            if node not in gate_names:
                continue

            others = [name for name in gate_names if name != node]
            # Count how many neighbors are in the source and destination partitions
            from_count = sum(1 for name in others if current_partition[name] == from_part)
            to_count = sum(1 for name in others if current_partition[name] == to_part)

            # FM Gain Logic:
            # If moving the node makes it the first node of the net in the 'to' side, 
            # we might increase the cut. If moving it removes the last node from 
            # the 'from' side, we decrease the cut.
            if from_count == 0: gain -= 1 
            if to_count == 0: gain += 1   

        return gain

    # Track the globally best state across all passes
    best_cut = get_cut_cost(partition)
    best_partition = partition.copy()

    # --- Iterative Improvement (Passes) ---
    for _ in range(10): # Execute up to 10 optimization passes
        # Save the state at the beginning of this FM pass
        pass_start_partition = partition.copy()
        locked = set()
        current_area0 = sum(V[g]._area for g in nodes if partition[g] == 0)
        moves = [] # Sequence of (node_moved, cut_cost_after_move)

        while len(locked) < len(nodes):
            best_move_node = None
            max_gain = -float('inf')

            # Selection: Find the unlocked node with highest gain that satisfies area balance
            for node in nodes:
                if node in locked: continue

                node_area = V[node]._area
                # Check if moving the node would violate Amin/Amax constraints
                if partition[node] == 0:
                    if current_area0 - node_area < Amin: continue
                else:
                    if current_area0 + node_area > Amax: continue

                gain = calculate_gain(node, partition)
                if gain > max_gain:
                    max_gain = gain
                    best_move_node = node

            # If no legal moves are available, terminate the current pass
            if best_move_node is None: break

            # Execute the move and lock the node for the remainder of this pass
            locked.add(best_move_node)
            partition[best_move_node] = 1 - partition[best_move_node]
            
            # Update area tracking for the next iteration
            if partition[best_move_node] == 0:
                current_area0 += V[best_move_node]._area
            else:
                current_area0 -= V[best_move_node]._area

            # Record the move and the resulting cut cost to allow rollback
            moves.append((best_move_node, get_cut_cost(partition)))
        
        # --- Pass Rollback ---
        # Find the point in the move sequence that yielded the lowest cut cost
        min_pass_cut = best_cut
        best_move_index = -1
        
        for i, (m_node, m_cost) in enumerate(moves):
            if m_cost < min_pass_cut:
                min_pass_cut = m_cost
                best_move_index = i
        
        # If an improvement was found, update best_partition and best_cut
        if best_move_index != -1:

            # Restore the partition at the beginning of this pass
            partition = pass_start_partition.copy()

            # Replay moves up to the best point of this pass
            for i in range(best_move_index + 1):
                m_node = moves[i][0]
                partition[m_node] = 1 - partition[m_node]

            best_partition = partition.copy()
            best_cut = min_pass_cut

        else:
            # No improvement was found in this pass
            break
        
    # --- Output Preparation ---
    # Construct lists of Vertex objects as required by the testing loop
    p0 = [V[g] for g in nodes if best_partition[g] == 0]
    p1 = [V[g] for g in nodes if best_partition[g] == 1]
    
    return [p0, p1], best_cut