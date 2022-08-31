package main

import "fmt"

func nonMaintainableFunction(
	varA bool,
	varB bool,
	varC bool,
	varD bool,
	printVars bool,
	printInvertedVars bool,
	printPairs bool,
	printInvertedPairs bool,
	printTriplets bool,
	printInvertedTriplets bool,
) []bool {
	fmt.Print("This ")
	fmt.Print("is ")
	fmt.Print("an ")
	fmt.Print("example ")
	fmt.Print("of ")
	fmt.Print("non-maintainable ")
	fmt.Println("function.")
	if !printVars {
		return []bool{varA, varB, varC, varD}
	}
	fmt.Println("Vars:")
	fmt.Println(varA)
	fmt.Println(varB)
	fmt.Println(varC)
	fmt.Println(varD)
	notA := !varA
	notB := !varB
	notC := !varC
	notD := !varD
	if !printInvertedVars {
		return []bool{notA, notB, notC, notD}
	}
	fmt.Println("Inverted vars:")
	fmt.Println(notA)
	fmt.Println(notB)
	fmt.Println(notC)
	fmt.Println(notD)
	aAndB := varA && varB
	aAndC := varA && varC
	aAndD := varA && varD
	bAndC := varB && varC
	bAndD := varB && varD
	cAndD := varC && varD
	if !printPairs {
		return []bool{aAndB, aAndC, aAndD, bAndC, bAndD, cAndD}
	}
	fmt.Println("Pairs:")
	fmt.Println(aAndB)
	fmt.Println(aAndC)
	fmt.Println(aAndD)
	fmt.Println(bAndC)
	fmt.Println(bAndD)
	fmt.Println(cAndD)
	notAAndB := !(varA && varB)
	notAAndC := !(varA && varC)
	notAAndD := !(varA && varD)
	notBAndC := !(varB && varC)
	notBAndD := !(varB && varC)
	notCAndD := !(varC && varD)
	if !printInvertedPairs {
		return []bool{notAAndB, notBAndC, notAAndD, notBAndC, notBAndD, notCAndD}
	}
	fmt.Println("Inverted pairs:")
	fmt.Println(notAAndB)
	fmt.Println(notAAndC)
	fmt.Println(notAAndD)
	fmt.Println(notBAndC)
	fmt.Println(notBAndD)
	fmt.Println(notCAndD)
	aAndBAndC := varA && varB && varC
	aAndBAndD := varA && varB && varD
	aAndCAndD := varA && varC && varD
	if !printTriplets {
		return []bool{aAndBAndC, aAndBAndD, aAndCAndD}
	}
	fmt.Println("Triplets:")
	fmt.Println(aAndBAndC)
	fmt.Println(aAndBAndD)
	fmt.Println(aAndCAndD)
	notAAndBAndC := !(varA && varB && varC)
	notAAndBAndD := !(varA && varB && varD)
	notAAndCAndD := !(varA && varC && varD)
	if !printInvertedTriplets {
		return []bool{notAAndBAndC, notAAndBAndD, notAAndCAndD}
	}
	fmt.Println("Inverted triplets:")
	fmt.Println(notAAndBAndC)
	fmt.Println(notAAndBAndD)
	fmt.Println(notAAndCAndD)
	return []bool{}
}

func main() {
	nonMaintainableFunction(true, true, true, true, true, true, true, true, true, true)
}
