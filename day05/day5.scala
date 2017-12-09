import scala.io.Source
import scala.annotation.tailrec

type Board = Vector[Int]
case class Turn(board: Board, pos: Int = 0,
                turnNum: Int = 0, done: Boolean = false)

def nextTurn(turn: Turn): Turn = turn match {
  case Turn(board, pos, turnNum, done) =>
    val move = board(pos)
    val newBoard = board.updated(pos, update(move))
    val newPos = pos + move
    val done = newPos < 0 || newPos >= board.length
    Turn(newBoard, newPos, turnNum+1, done)
}

def newVal1(old: Int): Int = old + 1
def newVal2(old: Int): Int = if (old < 3) old+1 else old-1

def play(board: Board): Int = {
  val firstTurn = Turn(board)
  val lastTurn = play(firstTurn)
  lastTurn.turnNum
}

@tailrec
def play(turn: Turn): Turn = turn match {
  case t @ Turn(_,_,_,true) => t
  case t => play(nextTurn(t))
}

val part = 2
val update = if (part == 1) newVal1 _ else newVal2 _
val testResult = if (part == 1) 5 else 10

val testBoard = Vector(0,3,0,1,-3)
assert(testResult == play(testBoard))

val input = Source.fromFile("input")
val board = input.getLines.map(_.toInt).toVector
println(play(board))

