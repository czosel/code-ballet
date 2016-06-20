import Html exposing (text)
import String

main =
      text (move 4 "A" "C" "B")

move n from to with = 
    case n of
        1 -> 
            from ++ "->" ++ to ++ " | "
        _ ->
            String.concat [
                move (n-1) from with to,
                move 1 from to with,
                move (n-1) with to from
            ]
