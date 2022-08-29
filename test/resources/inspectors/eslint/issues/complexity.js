function complexFunction(a, b, c, d) {
    if (a > b) {
        if (a > c) {
            if (a > d) {
                console.log("'a' is the largest!")
            }
        }
    }

    if (b > a) {
        if (b > c) {
            if (b > d) {
                console.log("'b' is the largest!")
            }
        }
    }

    if (c > a) {
        if (c > b) {
            if (c > d) {
                console.log("'c' is the largest!")
            }
        }
    }

    if (d > a) {
        if (d > b) {
            if (d > c) {
                console.log("'d' is the largest!")
            }
        }
    }
}
