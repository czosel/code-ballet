import json
import pprint

info = json.load(open('3.json'))

women       = info['women']
men         = info['men']
preferences = info['preferences']

women_prefs = {k: v for k, v in preferences.items() if k in women}
men_prefs   = {k: v for k, v in preferences.items() if k in men}

def invert_preferences(preferences):
    """
    Invert a preference set of one group, i.e.
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
    def choose(offers, prefs):
        """
        choose the favorite from an array of options, i.e.
        offers : [y, z]
        prefs  : [x, y, z]
        result : y
        """
        filtered = [name for name in offers if name in prefs]
        return filtered[0] if len(filtered) else None

    return {man: choose(offers, preferences[man]) for man, offers in inverted_prefs[0].items()}

inv = invert_preferences(women_prefs)
pprint.pprint(inv)
pprint.pprint(choose_preferred(inv))
