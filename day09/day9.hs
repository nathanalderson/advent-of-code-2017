import System.IO
import qualified Data.Map as Map
import Control.Exception
import Debug.Trace

data State = State { content :: String,
                     score :: Int,
                     level :: Int,
                     garbage :: Bool,
                     cancelled :: Bool,
                     garbageCount :: Int
                   } deriving (Show)

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
    mapM (uncurry runTest) tests
    putStrLn $ "score = " ++ show (getScore (State content 0 1 False False 0))
    hClose handle

runTest :: Int -> String -> IO String
runTest expectedScore input = do
    let score = fst . getScore $ State input 0 1 False False 0
        output = input ++ " = " ++ show score ++
                 " (" ++ show expectedScore ++ ")"
    putStrLn output
    assert (score == expectedScore) $ return output

getScore :: State -> (Int, Int)
getScore (State [] score _ _ _ garbageCount) = (score, garbageCount)
getScore (State (x:xs) s l g True gc) =
    getScore (State xs s l g False gc)

getScore (State ('!':xs) s l True c gc) =
    getScore (State xs s l True True gc)

getScore (State ('>':xs) s l True c gc) =
    getScore (State xs s l False c gc)

getScore (State ('<':xs) s l False c gc) =
    getScore (State xs s l True c gc)

getScore (State ('{':xs) s l False c gc) =
    getScore (State xs (s+l) (l+1) False c gc)

getScore (State ('}':xs) s l False c gc) =
    getScore (State xs s (l-1) False c gc)

getScore (State (x:xs) s l False c gc) =
    getScore (State xs s l False c gc)

getScore (State (x:xs) s l True c gc) =
    getScore (State xs s l True c (gc+1))

