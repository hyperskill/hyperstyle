package main

import (
	"errors"
	"fmt"
	"io/ioutil"
)

func returnError() error {
	return errors.New("empty name")
}

func main() {
	fmt.Println("Ignoring error")

	returnError()
	_ = returnError()

	ioutil.ReadFile("test.go")
	content, _ := ioutil.ReadFile("test.go")

	var someInterface interface{}
	stringInterface1 := someInterface.(string)
	stringInterface1 = someInterface.(string)

	stringInterface2, _ := someInterface.(string)
	stringInterface2, _ = someInterface.(string)

	fmt.Println(content, stringInterface1, stringInterface2)
}
