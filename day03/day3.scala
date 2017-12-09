// ring   size range  range-1   max
// 0      1    1      0         8*0
// 1      8    2-9    1-8       8*1
// 2      16   10-25  9-24      8*3
// 3      24   26-49  25-48     8*8
// 4      32   50-81  49-80     8*10
//
// 65                            57
//    37 36  35  34  33  32  31
//    38 17  16  15  14  13  30
//    39 18   5   4   3  12  29
//    40 19   6   1   2* 11  28  53
//    41 20   7   8   9  10* 27
//    42 21  22  23  24  25  26*
//    43 44  45  46  47  48  49  50*
// 73                            81

case class Ring(min: Int, max: Int, r: Int)

// what's the size of a ring
def size(r: Int): Int = r match {
  case 0 => 1
  case x => x*8
}

// what's the range of a ring: (min, max)
def range(r: Int): (Int, Int) = r match {
  case 0 => (1,1)
  case x =>
    val min = range(r-1)._2 + 1
    val max = min + size(r) - 1
    (min,max)
}

// an infinite lazy stream of rings: ((min, max), ring_num)
def rings = Stream.from(0).map(range).zipWithIndex.map {
  case ((min, max), r) => Ring(min, max, r)
}

// what ring is a value in. This is the radius part of the manhattan distance
def getRing(i: Int): Ring = {
  (rings.find {
    case Ring(min, max, r) => i >= min && i <= max
  }).get
}

// how long is one side of a given ring
def sideSize(r: Int): Int = r*2 + 1

// what are the 4 midpoints (theta of zero) of a given ring
def midpoints(ring: Ring): List[Int] = {
  val first = ring.min + (ring.r-1)
  val offset = sideSize(ring.r) - 1
  List(first, first+offset, first+(offset*2), first+(offset*3))
}

// what's the theta of a value given the ring its in
def getTheta(i: Int, ring: Ring): Int = {
  val mids = midpoints(ring)
  val offsets = mids.map(i-_).map(math.abs)
  offsets.min
}

def dist(i: Int): Int = {
  val ring = getRing(i)
  val theta = getTheta(i, ring)
  ring.r + theta
}

assert(dist(2) == 1)
assert(dist(10) == 3)
assert(dist(73) == 8)

//part 1
val input = 277678
println(dist(input))

// part 2

