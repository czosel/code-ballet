

function move(n, a="A", b="B", c="C") {
    if (n === 1)
        return [[a, b]]
    else
        return [].concat(
            move(n-1, a, c, b),
            move(1, a, b, c),
            move(n-1, c, a, b)
        )
}

function memoizableMove(n, a, b, c) {
    if (n === 1)
        return [[a, b]]
    else
        return [].concat(
            swap(move(n-1), b, c),
            move(1),
            swap(swap(move(n-1), a, c), a, b)
        )
}

function swap(moves, a, b) {
    return moves.map(move => {
        return move.map(pos => {
            return pos === a ? b :
                pos === b ? a :
                pos
        })
    })
}

console.log(memoizableMove(3, "A", "B", "C"))
