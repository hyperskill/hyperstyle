package main

import (
	"fmt"
	"strings"
)

// staticcheck-SA4026
const TEST = -0.0

func main() {
	fmt.Println(TEST)

	// staticcheck-SA4013
	if !!true {
		fmt.Println("Not true.")
	} else {
		fmt.Println("Not not true.")
	}

	// staticcheck-SA1018
	fmt.Println(strings.Replace("Hello, World!", "l", "", 0))
}
