import json
import pprint
import collections

class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2

info = json.load(open('3.json'))

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
        for man, offers in inverted_prefs[round_nr].items():
            chosenWoman = choose(offers + [engagements[man]])
            if (chosenWoman in engagements[man]):
               removeEngage 
        engagements = {man: choose(offers + [engagements[man]], preferences[man]) for man, offers in inverted_prefs[round_nr].items()}
        round_nr += 1
        #pprint.pprint(engagements)
    return engagements

def solve_procedural():
    def getUnmatchedWoman(engagements):
        """
        return the first woman without a partner or None
        """
        for woman in women:
            if woman not in engagements:
                return woman
        return None
    
    def is_preferred(prefs, a, b):
        return prefs.index(a) < prefs.index(b)

    engagements = TwoWayDict()
    proposals = women_prefs.copy()
    w = getUnmatchedWoman(engagements)
    while w:
        m = proposals[w].pop(0)
        print(w, 'asks', m)
        if m not in engagements:
            engagements[w] = m
            print(m, 'new', w)
        else:
            if is_preferred(men_prefs[m], w, engagements[m]):
                del engagements[m]
                engagements[w] = m
                print(m, 'prefs', w)
            else:
                print(m, 'rejects', w)
        w = getUnmatchedWoman(engagements)
    return engagements

inv = invert_preferences(women_prefs)
pprint.pprint(inv)
result = choose_preferred(inv)
print('functional result:')
pprint.pprint(result)

print('procedural result:')
pprint.pprint(solve_procedural())
