package main

import (
	"math"
)

func hypotenuse(a int, b int) float64 {
	return math.Sqrt(math.Pow(float64(a), 2) + math.Pow(float64(b), 2))
}
