package main

import "fmt"

var unusedVar int

func unusedFunction() {

}

func factorial(n int) int {
	if n == 0 {
		return 1
	}

	return n * factorial(n-1)
}

func main() {
	fmt.Println("Hello, world!")
}
