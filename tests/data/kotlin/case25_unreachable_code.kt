fun main() {
    for (i in 1..2) {
        break
        println() // unreachable
    }

    throw IllegalArgumentException("message")
    println() // unreachable

    fun f() {
        return
        println() // unreachable
    }
}
