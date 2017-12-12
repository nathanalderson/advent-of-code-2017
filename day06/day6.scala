type Board = Vector[Int]
case class Turn(board: Board, seen: Set[Board] = Set[Board](),
  turnNum: Int = 0, done: Boolean = false)
{
  override def toString = s"Turn($board, ${seen.size}, $turnNum, $done)"
}

case class Result(lastTurn: Turn, cycleSize: Int)

def nextTurn(turn: Turn): Turn = turn match {
  case Turn(board, seen, turnNum, done) =>
    val newBoard = calcNewBoard(board)
    val done = seen.contains(newBoard)
    val newSeen = seen + newBoard
    Turn(newBoard, newSeen, turnNum+1, done)
}

def calcNewBoard(board: Board): Board = {
  val (_, maxIndex) = board.zipWithIndex.reduce((l,r)=> if (r._1>l._1) r else l)
  distribute(maxIndex, board)
}

def distribute(from: Int, board: Board): Board = {
  val num = board(from)
  val allGet = num / board.length
  val remainder = num % board.length
  val getOneExtra = (from+1 until from+1+board.length).map(_ % board.length).take(remainder)
  def add(elem: (Int, Int)) = {
    val (v,i) = elem
    val reset = if (i==from) -1 * board(i) else 0
    val extra = if (getOneExtra.contains(i)) 1 else 0
    v + allGet + reset + extra
  }
  board.zipWithIndex.map(add)
}

assert(distribute(1,Vector(1,2,3)) == Vector(2,0,4))
assert(distribute(2,Vector(1,2,3)) == Vector(2,3,1))
assert(distribute(2,Vector(1,2,4)) == Vector(3,3,1))

def play(turn: Turn): Result = {
  val turns = Stream.iterate(turn)(nextTurn)
  val lastTurn: Turn = turns.find(_.done).get
  val cycleStart: Turn = turns.find(_.board == lastTurn.board).get
  val cycleSize = lastTurn.turnNum - cycleStart.turnNum
  Result(lastTurn, cycleSize)
}

val testBoard = Vector(0,2,7,0)
val testResult = play(Turn(testBoard))
assert(5 == testResult.lastTurn.turnNum)
assert(4 == testResult.cycleSize)

val board = Vector(0,5,10,0,11,14,13,4,11,8,8,7,1,4,12,11)
val result = play(Turn(board))
println(s"part1 = ${result.lastTurn.turnNum}")
println(s"part2 = ${result.cycleSize}")

