payoff_matrix={
    (1,1):(3,3),
    (1,0):(0,5),
    (0,0):(1,1),
    (0,1):(5,0)
}

def play_game(s_i,s_j):

    return payoff_matrix[(s_i,s_j)]