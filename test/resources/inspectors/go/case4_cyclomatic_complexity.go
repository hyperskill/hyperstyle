package main

import "fmt"

func plus(number int, bias int) int {
	if number == 0 && bias == 0 {
		return 0
	}

	if number == 0 && bias == 1 {
		return 1
	}

	if number == 0 && bias == 2 {
		return 2
	}

	if number == 1 && bias == 0 {
		return 1
	}

	if number == 1 && bias == 1 {
		return 2
	}

	if number == 1 && bias == 2 {
		return 3
	}

	if number == 2 && bias == 0 {
		return 2
	}

	if number == 2 && bias == 1 {
		return 3
	}

	if number == 2 && bias == 2 {
		return 4
	}

	return -1
}

func main() {
	fmt.Println(plus(1, 1))
}
