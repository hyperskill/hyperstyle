package main

import "fmt"

func hello(name string) {
	name = "Jerry" // staticcheck-SA4009
	fmt.Printf("Hello, %s!", name)
}

func main() {
	hello("Teddy")
}
