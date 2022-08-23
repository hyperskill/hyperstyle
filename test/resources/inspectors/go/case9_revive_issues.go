package main

import "fmt"

func main() {
    // revive-var-naming
	var this_is_int int
	_, _ = fmt.Scan(&this_is_int)

    // revive-bool-literal-in-expr and revive-identical-branches
	if this_is_int > 0 && true {
		fmt.Println("this_is_int > 0")
	} else {
		fmt.Println("this_is_int > 0")
	}
}
