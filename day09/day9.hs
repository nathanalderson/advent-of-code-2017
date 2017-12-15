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
    -- mapM (uncurry runTest) tests
    putStrLn $ "score = " ++ show (getScore (State content 0 1 False False 0))
    let countTests = [(0, "<>"),
                      (17, "<random characters>"),
                      (3, "<<<<>"),
                      (2, "<{!>}>"),
                      (0, "<!!>"),
                      (0, "<!!!>>"),
                      (10, "<{o\"i!a,<{i<a>")
                     ]
    hClose handle

-- runTest :: Int -> String -> IO String
-- runTest expectedScore input = do
--     let score = getScore $ State input 0 1 False False 0
--         output = input ++ " = " ++ show score ++
--                  " (" ++ show expectedScore ++ ")"
--     putStrLn output
--     assert (score == expectedScore) $ return output

getScore :: State -> (Int, Int)
-- getScore s | trace ("getScore " ++ show s) False = undefined
getScore (State [] score _ _ _ garbageCount) = (score, garbageCount)
getScore (State (x:rest) score level garbage True garbageCount) =
    getScore (State rest score level garbage False garbageCount)

getScore (State ('!':rest) score level True cancelled garbageCount) =
    getScore (State rest score level True True garbageCount)

getScore (State ('>':rest) score level True cancelled garbageCount) =
    getScore (State rest score level False cancelled garbageCount)

getScore (State ('<':rest) score level False cancelled garbageCount) =
    getScore (State rest score level True cancelled garbageCount)

getScore (State ('{':rest) score level False cancelled garbageCount) =
    getScore (State rest (score+level) (level+1) False cancelled garbageCount)

getScore (State ('}':rest) score level False cancelled garbageCount) =
    getScore (State rest score (level-1) False cancelled garbageCount)

getScore (State (x:rest) score level False cancelled garbageCount) =
    getScore (State rest score level False cancelled garbageCount)

getScore (State (x:rest) score level True cancelled garbageCount) =
    getScore (State rest score level True cancelled (garbageCount+1))
