import numpy as np

def calculate_pagerank(interactions, d=0.85, max_iterations=100, tolerance=1e-6):
    """
    Calculates the importance of users based on their interaction counts using a PageRank algorithm.

    Args:
        interactions (list of tuples): A list where each tuple represents a directed interaction,
                                       e.g., [('Alice', 'Bob'), ('Bob', 'Carol')].
        d (float): The damping factor, typically set to 0.85.
        max_iterations (int): The maximum number of iterations to perform.
        tolerance (float): The convergence tolerance. Iterations stop when the change in ranks
                           is below this value.

    Returns:
        dict: A dictionary mapping each user to their final PageRank importance score.
    """
    # 1. Identify all unique users
    all_users = sorted(list(set(user for interaction in interactions for user in interaction)))
    if not all_users:
        return {}
    
    n = len(all_users)
    user_to_index = {user: i for i, user in enumerate(all_users)}

    # 2. Construct the adjacency matrix based on interaction counts
    # A[i, j] will be the number of interactions from user j to user i
    adjacency_matrix = np.zeros((n, n))
    for interactor, receiver in interactions:
        i = user_to_index[receiver]
        j = user_to_index[interactor]
        adjacency_matrix[i, j] += 1

    # 3. Handle "sink" nodes (users who don't interact with anyone)
    # These columns will sum to 0. We'll make them transition to all users equally
    # to prevent importance from "leaking" out of the system.
    column_sums = adjacency_matrix.sum(axis=0)
    sink_cols = np.where(column_sums == 0)[0]
    # For sink columns, create a uniform transition probability
    if len(sink_cols) > 0:
        adjacency_matrix[:, sink_cols] = 1.0 / n

    # 4. Normalize the matrix to create the stochastic transition matrix `M`
    # Divide each column by its sum
    m_matrix = adjacency_matrix / adjacency_matrix.sum(axis=0)

    # 5. Initialize the rank vector with uniform values
    ranks = np.full(n, 1.0 / n)

    # 6. Perform the iterative PageRank calculation
    for _ in range(max_iterations):
        old_ranks = ranks.copy()
        
        # The PageRank formula: v' = d * (M * v) + (1 - d) / N
        ranks = d * (m_matrix @ old_ranks) + (1 - d) / n
        
        # Check for convergence
        if np.linalg.norm(ranks - old_ranks, ord=1) < tolerance:
            break

    # 7. Map the final ranks back to users and sort them
    final_ranks = {user: rank for user, rank in zip(all_users, ranks)}
    
    # Sort users by score in descending order
    sorted_users = sorted(final_ranks, key=final_ranks.get, reverse=True)

    return sorted_users

if __name__ == '__main__':
    # Helper function to print scores
    def print_scores(title, ranked_users_list):
        print(f"\n--- {title} ---")
        if ranked_users_list:
            for i, user in enumerate(ranked_users_list):
                print(f"{i+1}. {user}")
        else:
            print("No users found.")

    # --- Step 1: Initial Set of Interactions ---
    # Using 'list of lists' as specified by the user ("double list")
    initial_interactions = [
        ['Alice', 'Bob'], ['Alice', 'Bob'], ['Alice', 'Bob'], # Alice -> Bob (3 times)
        ['Bob', 'Alice'], ['Bob', 'Alice'],                 # Bob -> Alice (2 times)
        ['Bob', 'Carol'], ['Bob', 'Carol'], ['Bob', 'Carol'], # Bob -> Carol (5 times)
        ['Bob', 'Carol'], ['Bob', 'Carol'],
        ['Carol', 'Alice'], # Carol -> Alice (1 time - reduced to lower Carol's initial rank)
        ['David', 'Alice'], # David is a "fan" of Alice but receives no interactions
        ['Eve', 'Frank'],   # Eve and Frank form a separate, small cluster
        ['Frank', 'Eve'],
    ]

    print("Calculating initial user importance based on interactions...")
    initial_ranked_users = calculate_pagerank(initial_interactions)
    print_scores("Initial User Importance Order", initial_ranked_users)

    # --- Step 2: Simulate New Interactions ---
    # A new interaction happens: Alice interacts significantly with Carol (to boost Carol's rank)
    new_interactions_to_add = [
        ['Alice', 'Carol'], ['Alice', 'Carol'], ['Alice', 'Carol'] # Alice -> Carol (3 times)
    ]
    print(f"\n--- Simulating new interactions: Alice interacts with Carol multiple times ---")
    
    # Create an updated list of all interactions
    updated_interactions = initial_interactions + new_interactions_to_add

    # --- Step 3: Recalculate PageRank with Updated Interactions ---
    print("\nRecalculating user importance with new interaction...")
    updated_ranked_users = calculate_pagerank(updated_interactions)
    print_scores("Updated User Importance Order", updated_ranked_users)

    print("\n--- Dynamic Update Interpretation ---")
    print(f"Notice how the user importance order changes after Alice interacts multiple times with Carol.")
    print("Specifically, Carol's rank should significantly increase as she receives importance from Alice (a high-ranked user).")
    print("This might shift her position relative to other users like Eve or Frank, demonstrating a change in order.")
    print("Alice's score might slightly decrease relative to others, as her outbound importance is now split towards Carol.")


