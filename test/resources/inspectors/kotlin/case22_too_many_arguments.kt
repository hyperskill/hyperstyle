import java.util.*

class ConsoleHelper(val scanner: Scanner) {
    // 6+ -- is bad
    fun askLine(
        msg1: String = "",
        msg1: String = "",
        msg1: String = "",
        msg1: String = "",
        msg1: String = "",
        msg1: String = ""
    ): String {
        if (msg != "") {
            this.print(msg)
        }
        return scanner.nextLine()
    }

    // < 6 -- is ok
    fun askLine2(
        msg1: String = "",
        msg1: String = "",
        msg1: String = "",
        msg1: String = "",
        msg1: String = ""
    ): String {
        if (msg != "") {
            this.print(msg)
        }
        return scanner.nextLine()
    }
}
