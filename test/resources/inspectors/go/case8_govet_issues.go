package main

import (
    "bytes"
    "fmt"
)

func main() {
    // govet-printf
	fmt.Printf("%b", "Hello!")

    // govet-unusedresult
    var buf bytes.Buffer
	buf.String()

	return

	// govet-unreachable
	fmt.Print("Unreachable!")
}
