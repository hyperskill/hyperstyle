package main

import "fmt"

func main() {
	var a int
	_, _ = fmt.Scan(&a)

	// stylecheck-ST1017
	if 1 == a {
		fmt.Println("a == 1")
	}

	// stylecheck-ST1015
	switch {
	case a > 0:
		fmt.Println("a > 0")
	default:
		fmt.Println("a == 0")
	case a < 0:
		fmt.Println("a < 0")
	}
}
