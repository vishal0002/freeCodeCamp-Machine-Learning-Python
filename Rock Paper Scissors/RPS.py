import random

def player(prev_play, opponent_history=[], play_order={}, move_stats={"R": 0, "P": 0, "S": 0},
           loss_streak=[0], response_map={}, game_round=[0]):
    
    game_round[0] += 1

    if not prev_play:
        prev_play = 'R'

    opponent_history.append(prev_play)
    move_stats[prev_play] += 1

    if len(opponent_history) >= 2:
        my_last = counter_move(opponent_history[-2])  # What we probably played
        if opponent_history[-1] == my_last:
            loss_streak[0] += 1
        else:
            loss_streak[0] = 0

    # n-gram sequence
    for n in range(3, 6):
        if len(opponent_history) >= n:
            seq = "".join(opponent_history[-n:])
            for move in 'RPS':
                key = seq + move
                play_order[key] = play_order.get(key, 0)

    if len(opponent_history) >= 5:
        recent_seq = "".join(opponent_history[-5:])
        play_order[recent_seq] = play_order.get(recent_seq, 0) + 1

    # Predict opponent's next move 
    prediction_scores = {'R': 0, 'P': 0, 'S': 0}
    for n in range(3, 6):
        if len(opponent_history) >= n:
            seq = "".join(opponent_history[-n:])
            for move in 'RPS':
                key = seq + move
                prediction_scores[move] += play_order.get(key, 0) * n

    # Fallback if prediction uncertain 
    if sum(prediction_scores.values()) == 0:
        prediction = max(move_stats, key=move_stats.get)
    else:
        prediction = max(prediction_scores, key=prediction_scores.get)

    # switch to randomization
    if loss_streak[0] >= 4 or (game_round[0] % 100 == 0 and random.random() < 0.2):
        return random.choice(['R', 'P', 'S'])
     
    return counter_move(prediction)

def counter_move(move):
    return {'R': 'P', 'P': 'S', 'S': 'R'}[move]
