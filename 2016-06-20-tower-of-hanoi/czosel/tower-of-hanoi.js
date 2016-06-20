// basic solution
function move(n, a = "A", b = "B", c = "C") {
    if (n === 1)
        return [
            [a, b]
        ]
    else
        return [].concat(
            move(n - 1, a, c, b),
            move(1, a, b, c),
            move(n - 1, c, a, b)
        )
}

// memoized solution
cache = {};
let hitCount = 0;
let missCount = 0;
function memoizableMove(n, a = "A", b = "B", c = "C") {
    if (n === 1) {
        return [
            [a, b]
        ]
    } else if (cache[n + a + b + c]) {
        hitCount++;
        return cache[n + a + b + c]
    } else {
        missCount++;
        const result = [].concat(
            swap(memoizableMove((n - 1)), b, c),
            memoizableMove(1),
            swap(swap(memoizableMove(n - 1), a, c), a, b)
        )
        cache[n + a + b + c] = result
        return result
    }
}

function swap(moves, a, b) {
    const map = {
        [a]: b,
        [b]: a
    }
    return moves.map(move => {
        return move.map(pos => {
            return map[pos] ? map[pos] : pos
        })
    })
}

// console.log(move(3, "A", "B", "C"))
console.log(memoizableMove(10, "A", "B", "C"))
console.log(`cache hit:miss ${hitCount}:${missCount}`)
