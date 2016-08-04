import json
import pprint

info = json.load(open('300.json'))

women       = info['women']
men         = info['men']
preferences = info['preferences']

women_prefs = {k: v for k, v in preferences.items() if k in women}
men_prefs   = {k: v for k, v in preferences.items() if k in men}

def invert_preferences(preferences):
    """
    Invert a preference set of one group (turn "x prefers a" into
    "a is prefered by x"), i.e.
    x: [a,c,b]
    y: [a,b,c]
    z: [a,c,b]

    [{
      a: [x,y,z]
      b: []
      c: []
    }, {
      a: [],
      b: [y],
      c: [z]
    }, {
      a: [],
      b: [z],
      c: [y]
    }]
    """
    def invert_round(round_nr):
        result = {name: [] for name in men}
        for woman, prefs in preferences.items():
            pref = prefs[round_nr]
            result[pref].append(woman)
        return result

    return [invert_round(n) for n in range(len(preferences))]

def choose_preferred(inverted_prefs):
    def countUnmatched(engagements):
        return len({k:v for k, v in engagements.items() if v == None})

    def choose(offers, prefs):
        """
        choose the favorite from an array of options, i.e.
        offers : [y, z]
        prefs  : [x, y, z]
        result : y
        """
        filtered = [name for name in prefs if name in offers]
        return filtered[0] if len(filtered) else None

    round_nr = 0
    engagements = {man: None for man in men}
    while countUnmatched(engagements) > 0:
        print('round', round_nr, 'unmatched', countUnmatched(engagements))
        engagements = {man: choose(offers + [engagements[man]], preferences[man]) for man, offers in inverted_prefs[round_nr].items()}
        round_nr = round_nr + 1

    return engagements

inv = invert_preferences(women_prefs)
#pprint.pprint(inv)
result = choose_preferred(inv)
print('done.')
#pprint.pprint(result)
