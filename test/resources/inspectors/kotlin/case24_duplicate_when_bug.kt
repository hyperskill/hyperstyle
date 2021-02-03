fun main() {
    // bad
    when (i) {
        1 -> println("one")
        1 -> println("one")
        else -> println("else")
    }

    // ok
    when (i) {
        1 -> println("one")
        2 -> println("two")
        else -> println("else")
    }
}
