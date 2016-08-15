import json
import numpy as np

info = json.load(open('300.json'))

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
    def cross_out(point):
        mutual_prefs[point[0]] = -1
        mutual_prefs[:,point[1]] = -1
        return mutual_prefs

    notdone = np.where(mutual_prefs >= 0)
    if(len(notdone[0]) == 1):
        return ((notdone[0][0], notdone[1][0]), )
    
    target = mutual_prefs[mutual_prefs > 0].min()
    minima = np.transpose(np.where(mutual_prefs == target))[0]

    return solve(cross_out(minima)) + (tuple(minima), )

women_matrix = as_matrix(women_prefs, men)
men_matrix = as_matrix(men_prefs, women)

mutual_prefs = np.add(women_matrix, men_matrix.transpose())

#print(women_matrix)
#print(men_matrix)
#print(mutual_prefs)
result = solve(mutual_prefs)
print([women[r[0]] + '+' + men[r[1]] for r in result])
