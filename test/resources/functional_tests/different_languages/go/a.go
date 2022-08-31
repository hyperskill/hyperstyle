package main

import "fmt"

func hello(name string) string {
	if "Jerry" == name {
		return "Hello, Jerry!"
	} else {
		return "Hello, non-Jerry!"
	}
	return "Hello?"
}

func main() {
	var name string
	fmt.Scan(&name)
	fmt.Println(hello(name))
}
