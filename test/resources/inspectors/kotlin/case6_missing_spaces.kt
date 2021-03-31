import java.util.Scanner

fun main() {
    val scanner = Scanner(System.`in`)

    val a: Int = scanner.nextInt()
    val b:Int = scanner.nextInt()
    val c : Int = scanner.nextInt()

    //some operations below
    println(a+b)
    println(a- b)
    println("${a *b} ml of water")

    val q: Int ? = null // should be space
}
