import java.util.Scanner

class Main {
    val yes = "YES"
    val no = "NO"

    fun main() {
        printArmy()
        checkTriangle()
        checkQueens()
        calculator()
    }

    // CC is 10
    fun printArmy() {
        val scanner = Scanner(System.`in`)
        val p = scanner.nextInt()
        if (p < 1) {
            println("no army")
        } else if (p < 5) {
            println("few")
        } else if (p < 10) {
            println("several")
        } else if (p < 20) {
            println("pack")
        } else if (p < 50) {
            println("lots")
        } else if (p < 100) {
            println("horde")
        } else if (p < 250) {
            println("throng")
        } else if (p < 500) {
            println("swarm")
        } else if (p < 1000) {
            println("zounds")
        } else {
            println("legion")
        }
    }

    fun checkTriangle() { // CC is 4
        val scanner = Scanner(System.`in`)

        val a = scanner.nextInt()
        val b = scanner.nextInt()
        val c = scanner.nextInt()

        if (a + b > c && b + c > a && c + a > b) {
            println(yes)
        } else {
            println(no)
        }
    }

    fun checkQueens() { // CC is 4
        val scanner = Scanner(System.`in`)

        val num1 = scanner.nextInt()
        val num2 = scanner.nextInt()
        val num3 = scanner.nextInt()
        val num4 = scanner.nextInt()

        if (num1 == num3) {
            println(yes)
        } else if (num2 == num4) {
            println(yes)
        } else if (Math.abs(num1 - num3) == Math.abs(num2 - num4)) {
            println(NO)
        } else {
            println(no)
        }
    }

    fun calculator() { // CC is 3
        val scanner = Scanner(System.`in`)

        val line = scanner.nextLine().split("\\s+")

        val a = Long.parseLong(line[0])
        val op = line[1].charAt(0)
        val b = Long.parseLong(line[2])

        when (op) {
            '+' -> println(a + b)
            '-' -> println(a - b)
            '*' -> println(a * b)
            '/' -> {
                if (b == 0) {
                    println("Division by 0!")
                } else {
                    println(a / b)
                }
            else -> println("Unknown operator")
        }
    }
}
