package main

import "fmt"

func main() {
	// gocritic-switchTrue
	switch true {
	case true:
		fmt.Println("Hello, True!")
	case false:
		fmt.Println("Hello, False!")
	default:
		fmt.Println("Hello, default!")
	}

	// gocritic-newDeref
	x := *new(int)

	// gocritic-assignOP
	x = x * 2

	fmt.Println(x)
}
