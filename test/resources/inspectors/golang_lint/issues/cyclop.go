package main

import "fmt"

func main() {
	var a int
	var b int
	var c int
	var d int

	fmt.Scan(&a)
	fmt.Scan(&b)
	fmt.Scan(&c)
	fmt.Scan(&d)

	if a > b {
		if a > c {
			if a > d {
				fmt.Println("'a' is the largest.")
			}
		}
	}

	if b > a {
		if b > c {
			if b > d {
				fmt.Println("'b' is the largest.")
			}
		}
	}

	if c > a {
		if c > b {
			if c > d {
				fmt.Println("'c' is the largest.")
			}
		}
	}

	if d > a {
		if d > b {
			if d > c {
				fmt.Println("'d' is the largest.")
			}
		}
	}
}
