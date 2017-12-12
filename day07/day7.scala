import scala.io.Source

case class Program(name: String, weight: Int)
case class Node(program: Program, children: List[Node])
case class SimpleNode(program: Program, childNames: List[String])

val input = Source.fromFile("input")
case class InputLine(name: String, weight: Int, children: List[String])

def parseNode(s: String): (String, Int) = {
  val re = """(\w+) \((\d+)\)""".r
  s match {
    case re(name, weight) => (name, weight.toInt)
    case _ => throw new Exception("Parse error on '$s'")
  }
}

def parseLine(line: String): InputLine = {
  line.split(" -> ") match {
    case Array(node) =>
      val nodeInfo = parseNode(node)
      InputLine(nodeInfo._1, nodeInfo._2, List())
    case Array(node, children) =>
      val nodeInfo = parseNode(node)
      InputLine(nodeInfo._1, nodeInfo._2, children.split(", ").toList)
  }
}

val inputLines = input.getLines.map(parseLine)
type NodeMap = Map[String, SimpleNode]

def buildNodeMap(inputLines: Iterator[InputLine]): NodeMap = {
  inputLines.map {
    case InputLine(name, weight, childNames) =>
      (name -> SimpleNode(Program(name, weight), childNames))
  }.toMap
}

def getParent(name: String, nodeMap: NodeMap): Option[SimpleNode] =
  nodeMap.valuesIterator.find { _.childNames.contains(name) }

def getRoot(nodeMap: NodeMap): SimpleNode =
  nodeMap.find { case (name, snode) =>
    getParent(name, nodeMap) == None
  }.get._2

def buildTree(nodeMap: NodeMap)(root: SimpleNode): Node = root match {
  case SimpleNode(program, childNames) =>
    val childSnodes = childNames.map(nodeMap)
    Node(program, childSnodes.map(buildTree(nodeMap)))
}

// (majority, minority, minorityIndex)
def majorMinor(l: List[Int]): (Int, Int, Int) = {
  if (l.length == 1)
    throw new Exception("singular value")
  val (val1, val2) = (l.head, l.find(_!=l.head).get)
  val (maj, min) = if (l.count(_==val1) == 1)
    (val2, val1)
  else
    (val1, val2)
  val minIndex = l.zipWithIndex.find(_._1==min).get._2
  (maj, min, minIndex)
}

def findUnbalanced(root: Node): Either[Int, Int] = {
  val rval = root match {
    case Node(prog, List()) => Left(prog.weight)
    case Node(prog, children) =>
      val subTreeWeights = children.map(findUnbalanced)
      subTreeWeights.find(_.isRight).getOrElse {
        val weights = subTreeWeights.map(_.left.get)
        if (weights.toSet.size == 1) {
          Left(weights.sum + prog.weight)
        } else {
          val (maj, min, minIndex) = majorMinor(weights)
          Right(children(minIndex).program.weight + (maj-min))
        }
      }
  }
  rval
}

val testInput = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

assert(parseLine("pbga (66)") == InputLine("pbga", 66, List()))
assert(parseLine("fwft (72) -> ktlj, cntj, xhth") ==
  InputLine("fwft", 72, List("ktlj", "cntj", "xhth")))

val testNodeMap: NodeMap = buildNodeMap(testInput.lines.map(parseLine))
val testRoot = getRoot(testNodeMap)
val testTree = buildTree(testNodeMap)(testRoot)
val testUnbalanced = findUnbalanced(testTree)
assert(testUnbalanced == Right(60))

val nodeMap: NodeMap = buildNodeMap(inputLines)
val root = getRoot(nodeMap)
println(s"root = ${root.program.name}")
val tree = buildTree(nodeMap)(root)
val unbalanced = findUnbalanced(tree)
println(s"part2 = $unbalanced")
