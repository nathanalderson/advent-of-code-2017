import System.IO
import qualified Data.Map as Map

main = do
    handle <- openFile "input" ReadMode
    content <- hGetContents handle
    let tests = [(1, "{}"),
                 (6, "{{{}}}"),
                 (5, "{{},{}}"),
                 (16, "{{{},{},{{}}}}"),
                 (1, "{<a>,<a>,<a>,<a>}"),
                 (9, "{{<ab>},{<ab>},{<ab>},{<ab>}}"),
                 (9, "{{<!!>},{<!!>},{<!!>},{<!!>}}"),
                 (3, "{{<a!>},{<a!>},{<a!>},{<ab>}}")
                ]
    hClose handle

runTest :: Int -> String -> IO Int
runTest expectedScore input = do
    let score = getScore input
    putStrLn $ input ++ " = " ++ show score ++
               " (should be " ++ show expectedScore ++ ")"
    return score

getScore :: String -> Int
getScore input = undefined
