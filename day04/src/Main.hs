module Main where

import System.IO
import Data.List

main = do
    handle <- openFile "input" ReadMode
    contents <- hGetContents handle
    let valids = validPassphrases contents
        numValids = length valids
    print numValids
    hClose handle

validPassphrases :: String -> [String]
validPassphrases input =
    let allLines = lines input
    in filter isValid allLines

isValid :: String -> Bool
isValid s =
    let allWords = words s
        uniqueWords = nub (map sort allWords)
    in (length allWords) == (length uniqueWords)
