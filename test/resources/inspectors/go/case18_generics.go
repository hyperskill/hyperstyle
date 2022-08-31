package main

import "fmt"

func generic_sum[K comparable, V int | float64](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}

func main() {
	fmt.Println(generic_sum(map[string]int{"first": 42, "second": 69}))
	fmt.Println(generic_sum(map[string]float64{"first": 42.69, "second": 69.42}))
}
