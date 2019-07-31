import random

def play_game(p, n, R):
  total_card_count = 52
  undealt_cards = range(total_card_count)
  your_cards = []
  opponent_cards = []
  your_cards.append(undealt_cards.pop(R))  # take card in question
  dealt_card_target = n*p
  dealt_card_count = 1
  while dealt_card_count < dealt_card_target:
    rand_index = random.randint(0, len(undealt_cards)-1)
    card = undealt_cards.pop(rand_index)
    if len(your_cards) < n:
      if card < R:  # don't accept any stronger cards
        undealt_cards.append(card)
        continue
      your_cards.append(card)
    else:
      opponent_cards.append(card)
    dealt_card_count +=1
  for rank in range(R):  # check if any stronger cards dealt to opponents
    if rank in opponent_cards:
      return False  # card is not strongest
  return True  # card is strongest

def simulate(p, n, R, iterations):
  print('playing %d games of p: %d, n: %d, R: %d' % (iterations, p, n, R))
  strongest = 0
  for i in range(iterations):
    strongest += 1 if play_game(p, n, R) else 0
  print('-> card rank %d is strongest in %.3f%% of games' % (R, 100.0*strongest/iterations))

simulate(5, 3, 1, 1000000)
simulate(5, 3, 2, 1000000)
simulate(2, 1, 3, 1000000)
simulate(6, 6, 3, 1000000)
