import json
import pprint
import numpy as np

info = json.load(open('3.json'))

women       = info['women']
men         = info['men']
preferences = info['preferences']

women_prefs = {k: v for k, v in preferences.items() if k in women}
men_prefs   = {k: v for k, v in preferences.items() if k in men}

def as_matrix(prefs, subjects):
    def numeric(prefList, subjects):
        return [subjects.index(subject) for subject in prefList]
    return np.matrix([numeric(prefList, subjects) for person, prefList in prefs.items()])

def solve(mutual_prefs):
    import ipdb; ipdb.set_trace()
    notdone = np.where(mutual_prefs < float('inf'))
    if(len(notdone[0]) == 1):
        print(women[notdone[0][0]], men[notdone[1][0]])
        return
    def cross_out(point):
        mutual_prefs[point[0]] = float('inf')
        mutual_prefs[:,point[1]] = float('inf')
        return mutual_prefs

    minima = np.transpose(np.where(mutual_prefs == mutual_prefs.min()))[0]
    print(minima)
    print(women[minima[0]], men[minima[1]])
    print('crossed', cross_out(minima))
    return solve(cross_out(minima))

women_matrix = as_matrix(women_prefs, men)
men_matrix = as_matrix(men_prefs, women)

mutual_prefs = np.add(women_matrix, men_matrix.transpose())

print(women_matrix)
print(men_matrix)
print(mutual_prefs)
solve(mutual_prefs)
