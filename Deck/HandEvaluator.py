from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.
def evaluate_hand(hand: list[Card]):
    ranks = []
    suits = []

    for card in hand:
        ranks.append(card.rank.value)
        suits.append(card.suit)

    rank_counts = {}
    for r in ranks:
        if r not in rank_counts:
            rank_counts[r] = 0
        rank_counts[r] += 1

    counts_sorted = sorted(rank_counts.values(), reverse=True)

    suit_counts = {}
    for s in suits:
        if s not in suit_counts:
            suit_counts[s] = 0
        suit_counts[s] += 1

    is_flush = False
    flush_suit = None
    for s, count in suit_counts.items():
        if count >= 5:
            is_flush = True
            flush_suit = s
            break

    unique_ranks = sorted(list(set(ranks)))

    def has_straight(rank_list):
        if len(rank_list) < 5:
            return False

        consecutive = 1
        for i in range(1, len(rank_list)):
            if rank_list[i] == rank_list[i - 1] + 1:
                consecutive += 1
            else:
                consecutive = 1

            if consecutive >= 5:
                return True

        return False

    is_straight = has_straight(unique_ranks)

    if not is_straight and 14 in unique_ranks:
        low_ace = [1 if r == 14 else r for r in unique_ranks]
        low_ace = sorted(list(set(low_ace)))
        is_straight = has_straight(low_ace)

    is_straight_flush = False
    if is_flush:
        suited_ranks = []
        for card in hand:
            if card.suit == flush_suit:
                suited_ranks.append(card.rank.value)

        suited_unique = sorted(list(set(suited_ranks)))

        if has_straight(suited_unique):
            is_straight_flush = True
        else:
            if 14 in suited_unique:
                low_suited = [1 if r == 14 else r for r in suited_unique]
                low_suited = sorted(list(set(low_suited)))
                if has_straight(low_suited):
                    is_straight_flush = True

    if is_straight_flush:
        return "Straight Flush"
    if 4 in counts_sorted:
        return "Four of a Kind"
    if 3 in counts_sorted and 2 in counts_sorted:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if 3 in counts_sorted:
        return "Three of a Kind"
    if counts_sorted.count(2) >= 2:
        return "Two Pair"
    if 2 in counts_sorted:
        return "One Pair"

    return "High Card"
