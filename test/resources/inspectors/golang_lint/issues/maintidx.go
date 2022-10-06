package main

import "fmt"

func main() {
	var a int
	var b int
	var operator string

	fmt.Scan(&a)
	fmt.Scan(&b)
	fmt.Scan(&operator)

	if operator == "+" {
		if a == 0 && b == 0 {
			fmt.Print(0)
		} else if a == 0 && b == 1 {
			fmt.Print(1)
		} else if a == 0 && b == 2 {
			fmt.Print(2)
		} else if a == 1 && b == 0 {
			fmt.Print(1)
		} else if a == 1 && b == 1 {
			fmt.Print(2)
		} else if a == 1 && b == 2 {
			fmt.Print(3)
		} else if a == 2 && b == 0 {
			fmt.Print(2)
		} else if a == 2 && b == 1 {
			fmt.Print(3)
		} else if a == 2 && b == 2 {
			fmt.Print(4)
		} else {
			fmt.Print("I don't known :(")
		}
	} else if operator == "-" {
		if a == 0 && b == 0 {
			fmt.Print(0)
		} else if a == 0 && b == 1 {
			fmt.Print(-1)
		} else if a == 0 && b == 2 {
			fmt.Print(-2)
		} else if a == 1 && b == 0 {
			fmt.Print(1)
		} else if a == 1 && b == 1 {
			fmt.Print(0)
		} else if a == 1 && b == 2 {
			fmt.Print(-1)
		} else if a == 2 && b == 0 {
			fmt.Print(2)
		} else if a == 2 && b == 1 {
			fmt.Print(1)
		} else if a == 2 && b == 2 {
			fmt.Print(0)
		} else {
			fmt.Print("I don't know :(")
		}
	} else if operator == "*" {
		if a == 0 && b == 0 {
			fmt.Print(0)
		} else if a == 0 && b == 1 {
			fmt.Print(0)
		} else if a == 0 && b == 2 {
			fmt.Print(0)
		} else if a == 1 && b == 0 {
			fmt.Print(0)
		} else if a == 1 && b == 1 {
			fmt.Print(1)
		} else if a == 1 && b == 2 {
			fmt.Print(2)
		} else if a == 2 && b == 0 {
			fmt.Print(0)
		} else if a == 2 && b == 1 {
			fmt.Print(2)
		} else if a == 2 && b == 2 {
			fmt.Print(4)
		} else {
			fmt.Print("I don't know :(")
		}
	} else if operator == "/" {
		if a == 0 && b == 0 {
			fmt.Print("I don't know :(")
		} else if a == 0 && b == 1 {
			fmt.Print(0)
		} else if a == 0 && b == 2 {
			fmt.Print(0)
		} else if a == 1 && b == 0 {
			fmt.Print("o_0")
		} else if a == 1 && b == 1 {
			fmt.Print(1)
		} else if a == 1 && b == 2 {
			fmt.Print(1 / 2)
		} else if a == 2 && b == 0 {
			fmt.Print(0)
		} else if a == 2 && b == 1 {
			fmt.Print(2)
		} else if a == 2 && b == 2 {
			fmt.Print(1)
		} else {
			fmt.Print("I don't know :(")
		}
	} else {
		fmt.Print("I don't know :(")
	}
}
