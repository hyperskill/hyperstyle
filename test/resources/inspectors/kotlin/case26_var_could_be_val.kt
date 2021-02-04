fun example() {
    var i = 1 // violation: this variable is never re-assigned
    val j = i + 1
}

// ok
fun example() {
    val i = 1
    val j = i + 1

}
