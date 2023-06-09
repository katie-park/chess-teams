import codecs, json, sys

data = json.load(open('data.json'))

# sort *rated* players from lowest to highest rating
players = [p for p in data['players'] if p['rating'] != None]
players.sort(key=lambda p : p['rating'])

'''
brainstorming
* every player qualifies for a limited range of teams based off of the highest and lowest rated players available
* each team's board 1 should have a rating close to or higher than the limit
'''

def avg(lst):
    return int(sum(lst)/len(lst) * 100) / 100       # truncate to two decimal places

def json_player(name, rating, min_avg, max_avg):
    return {'name'  : name, 'rating' : rating, 'min' : min_avg, 'max' : max_avg}

# calculate lowest and highest rated team each player can be in
new_data = data
for p in range(len(players)):
    min_ps = [p['rating'] for p in players[0 : 4]]
    max_ps = [p['rating'] for p in players[len(players)-4 : len(players)]]

    # TO-DO: set top 4 player-based team rating as a global constant (prolly just cleaner)
    if p > 2:                                       # player not already in min
        min_ps.pop();
        min_ps.insert(0, players[p]['rating']);
    if p < len(players) - 3:                        # player not already in max
        max_ps.pop(0);
        max_ps.append(players[p]['rating'])
    
    min_avg = avg(min_ps)
    max_avg = avg(max_ps)
    
    unrated_players = [p for p in data['players'] if p['rating'] == None]
    for u in range(min(len(unrated_players), 3)):   # test teams with unrated players
        min_ps.pop()
        max_ps.pop(0)
        min_avg = min(min_avg, avg(min_ps))
        max_avg = max(max_avg, avg(max_ps))
    
    print(players[p]['name'].upper() + ' (' + str(players[p]['rating']) + ')')
    print('\tmin:\t' + str(min_avg) + '\t' + str(min_ps))
    print('\tmax:\t' + str(max_avg) + '\t' + str(max_ps) + '\n')

    new_data['players'][p] = json_player(players[p]['name'], players[p]['rating'], min_avg, max_avg)

# TO-DO: handle unrated players
for i in range(len(unrated_players)):
    min_avg_rating = avg(min_ps) if i > len(players) - 5 else avg(min_ps[0:3])
    max_avg_rating = max(avg(max_ps), avg(max_ps[0:3]))
    new_data['players'].append(json_player(unrated_players[i]['name'], unrated_players[i]['rating'], min_avg_rating, max_avg_rating))

# write to file
with open('output.json', 'w') as f:
  json.dump(new_data, f,  sort_keys=True, indent=4, separators=(',', ': '))

# TO-DO: team generation
sizes = range(data['teams']['min'], data['teams']['max'] + 1)   # potential team sizes