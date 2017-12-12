import qualified Data.Map as Map
import System.IO
import Control.Exception
import Debug.Trace

type Register = String
type Data = Int
type Registers = Map.Map Register Data

data Op = Inc | Dec
    deriving (Enum, Eq, Ord, Bounded)
instance Show Op where
    show Inc = "inc"
    show Dec = "dec"
instance Read Op where
    readsPrec _ "inc" = [(Inc,"")]
    readsPrec _ "dec" = [(Dec,"")]
    readsPrec _ _ = []

type Arg = Data

data Condition = Gt | Lt | Gte | Lte | Eq | Neq
    deriving (Enum, Eq, Ord, Bounded)
instance Show Condition where
    show Gt = ">"
    show Lt = "<"
    show Gte = ">="
    show Lte = "<="
    show Eq = "=="
    show Neq = "!="
instance Read Condition where
    readsPrec _ ">" = [(Gt,"")]
    readsPrec _ "<" = [(Lt,"")]
    readsPrec _ ">=" = [(Gte,"")]
    readsPrec _ "<=" = [(Lte,"")]
    readsPrec _ "==" = [(Eq,"")]
    readsPrec _ "!=" = [(Neq,"")]
    readsPrec _ _ = []

data Instruction = Instruction { reg :: Register,
                                 op :: Op,
                                 arg :: Arg,
                                 condReg :: Register,
                                 cond :: Condition,
                                 condArg :: Arg
                               } deriving (Eq, Ord)
instance Show Instruction where
    show (Instruction reg op arg condReg cond condArg) =
        reg ++ " " ++ show op ++ " " ++ show arg ++ " if " ++
            condReg ++ " " ++ show cond ++ " " ++ show condArg
instance Read Instruction where
    readsPrec _ input =
        let tokens = words input
            reg = tokens !! 0
            op = read (tokens !! 1) :: Op
            arg = read (tokens !! 2) :: Arg
            condReg = tokens !! 4
            cond = read (tokens !! 5) :: Condition
            condArg = read (tokens !! 6) :: Arg
         in [(Instruction reg op arg condReg cond condArg, "")]

main = do
    handle <- openFile "input" ReadMode
    content <- hGetContents handle
    let testContent = "b inc 5 if a > 1 \n\
                       \a inc 1 if b < 5 \n\
                       \c dec -10 if a >= 1 \n\
                       \c inc -20 if c == 10"
        testRegs = process testContent
        testLargest = maximum (Map.elems $ last testRegs)
        regs = process content
        largest = maximum (Map.elems $ last regs)
    -- return $ assert (testLargest == 1) ()
    -- print $ Map.assocs $ last testRegs
    putStrLn $ "test largest = " ++ show testLargest
    putStrLn $ "test largest ever = " ++ show (largestEver testRegs)
    -- print $ Map.assocs $ last regs
    putStrLn $ "largest = " ++ show largest
    putStrLn $ "largest ever = " ++ show (largestEver regs)
    hClose handle

largestEver :: [Registers] -> Data
largestEver regsList =
    let maxReg m | Map.null m = 0
        maxReg regs = maximum (Map.elems regs)
     in foldl (\acc regs -> max acc (maxReg regs)) 0 regsList

parseLine :: String -> Instruction
-- parseLine s | trace ("parseLine " ++ s) False = undefined
parseLine s = read s

getComparator :: Instruction -> (Arg -> Bool)
getComparator (Instruction _ _ _ _ cond condArg) =
    case cond of Gt -> (>condArg)
                 Lt -> (<condArg)
                 Gte -> (>=condArg)
                 Lte -> (<=condArg)
                 Eq -> (==condArg)
                 Neq -> (/=condArg)

getModifier :: Instruction -> (Data -> Data)
getModifier (Instruction _ op arg _ _ _) =
    case op of Inc -> (+arg)
               Dec -> (subtract arg)

doInstruction :: Registers -> Instruction -> Registers
-- doInstruction registers instruction | trace ("doInstruction " ++ show registers ++ " " ++ show instruction) False = undefined
doInstruction registers instruction =
    let comparator = getComparator instruction
        modifier = getModifier instruction
        alterFunc Nothing = Just $ modifier 0
        alterFunc (Just x) = Just $ modifier x
     in if comparator . getReg registers $ condReg instruction
           then Map.alter alterFunc (reg instruction) registers
           else registers

getReg :: Registers -> Register -> Data
getReg regs reg = Map.findWithDefault 0 reg regs

process :: String -> [Registers]
process content =
    let allLines = lines content
        parsedLines = map parseLine allLines
     in scanl doInstruction Map.empty parsedLines

