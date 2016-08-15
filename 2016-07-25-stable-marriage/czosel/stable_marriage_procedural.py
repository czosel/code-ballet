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

info = json.load(open('300.json'))

women       = info['women']
men         = info['men']
preferences = info['preferences']

women_prefs = {k: v for k, v in preferences.items() if k in women}
men_prefs   = {k: v for k, v in preferences.items() if k in men}

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
        #print(w, 'asks', m)
        if m not in engagements:
            engagements[w] = m
            #print(m, 'new', w)
        else:
            if is_preferred(men_prefs[m], w, engagements[m]):
                del engagements[m]
                engagements[w] = m
                #print(m, 'prefers', w)
            #else:
                #print(m, 'rejects', w)
        w = getUnmatchedWoman(engagements)
    return engagements

print('procedural result:')
pprint.pprint(solve_procedural())
