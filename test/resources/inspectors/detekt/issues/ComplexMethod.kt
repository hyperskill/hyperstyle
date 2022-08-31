fun main() {
    val a = readLine()?.toInt() ?: 0
    val b = readLine()?.toInt() ?: 0
    val c = readLine()?.toInt() ?: 0
    val d = readLine()?.toInt() ?: 0

    if (a > b) {
        if (a > c) {
            if (a > d) {
                println("'a' is the largest");
            }
        }
    }

    if (b > a) {
        if (b > c) {
            if (b > d) {
                println("'b' is the largest");
            }
        }
    }

    if (c > a) {
        if (c > b) {
            if (c > d) {
                println("'c' is the largest");
            }
        }
    }

    if (d > a) {
        if (d > b) {
            if (d > c) {
                println("'d' is the largest");
            }
        }
    }
}
