

def play_game(s_i, s_j, game_type):

    if game_type == 'PD':  # 囚徒
        payoff_matrix = {
            (1, 1): (3, 3),
            (1, 0): (0, 5),
            (0, 1): (5, 0),
            (0, 0): (1, 1),
        }
    elif game_type == "SD":  # 雪堆
        payoff_matrix = {
            (1, 1): (3, 3),
            (1, 0): (0, 4),
            (0, 1): (4, 0),
            (0, 0): (1, 1),
        }
    elif game_type == "SH":  # 猎鹿
        payoff_matrix = {
            (1, 1): (4, 4),
            (1, 0): (0, 3),
            (0, 1): (3, 0),
            (0, 0): (2, 2),
        }
    else:
        raise ValueError("Unknown game type")
    return payoff_matrix[(s_i, s_j)]
