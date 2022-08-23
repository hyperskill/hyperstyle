package main

import "fmt"

func printNumber(number int) {
	fmt.Println(number)
}

func main() {
	printNumber(42)

	var input int
	fmt.Scan(&input)

	if input == 1 {
		printNumber(input)
	}

	switch input {
	case 0:
		printNumber(input)
	case 1:
		printNumber(input)
	case 2:
		printNumber(input)
	case 3:
		printNumber(input)
	default:
		fmt.Println("I don't want to print this number!")
	}
}
