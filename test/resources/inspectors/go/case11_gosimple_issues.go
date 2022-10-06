package main

import "fmt"

func main() {
	// gosimple-S1006
	for true {
		fmt.Println("I am an infinity loop.")
	}

	var input string
	_, _ = fmt.Scan(&input)

	// gosimple-S1039
	input = fmt.Sprintf("My name is Jeff.")

	// gosimple-S1029
	for _, r := range []rune(input) {
		fmt.Println(r)
	}
}
