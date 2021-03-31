fun main() {
    // bad
    (1..10).forEach {
        println(it)
    }
    (1 until 10).forEach {
        println(it)
    }
    (10 downTo 1).forEach {
        println(it)
    }

    // ok
    for (i in 1..10) {
        println(i)
    }
}
