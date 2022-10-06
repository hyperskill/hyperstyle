package main

import "fmt"

func main() {
	var input int
	_, _ = fmt.Scan(&input)

	// stylecheck-ST1017
	if 1 == input {
		fmt.Println("input == 1")
	}

	// stylecheck-ST1015
	switch {
	case input > 0:
		fmt.Println("input > 0")
	default:
		fmt.Println("input == 0")
	case input < 0:
		fmt.Println("input < 0")
	}
}
