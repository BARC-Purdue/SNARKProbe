package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"

	ecc "github.com/cloudflare/circl/ecc/bls12381"
)

func ff(filename string) string {
	// Read data from input file
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}

	return string(content)
}

func g(filename string) []byte {
	// Read data from input file
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}

	slist := strings.Split(string(content), " ")

	var blist []byte

	for _, item := range slist {
		num, _ := strconv.Atoi(item)
		bnum := byte(num)

		blist = append(blist, bnum)
	}

	return blist
}

func toAffineG1(P *ecc.G1) *ecc.G1 {
	blist := P.Bytes()
	tmp := new(ecc.G1)
	tmp.SetBytes(blist)

	return tmp
}

func toAffineG2(P *ecc.G2) *ecc.G2 {
	blist := P.Bytes()
	tmp := new(ecc.G2)
	tmp.SetBytes(blist)

	return tmp
}

func main() {

	/* |-----------|---------|---------|---------|---------|---------|---------|---------|
	   | Parameter |    1    |    2    |    3    |    4    |    5    |    6    |    n    |
	   |-----------|---------|---------|---------|---------|---------|---------|---------|
	   | Operaions | g1 + g1 | g1 * ff | g2 + g2 | g2 * ff | ff + ff | ff * ff | Unused  |
	   |-----------|---------|---------|---------|---------|---------|---------|---------| */

	opindex, _ := strconv.Atoi(os.Args[1])

	filename1 := os.Args[2]
	filename2 := os.Args[3]

	if opindex == 1 {
		// g1 + g1

		P := new(ecc.G1)
		Q := new(ecc.G1)
		PQ := new(ecc.G1)

		// Set variable P
		g1_value1 := g(filename1)
		P.SetBytes(g1_value1)

		// Set variable Q
		g1_value2 := g(filename2)
		Q.SetBytes(g1_value2)

		// Calculate PQ = P + Q
		PQ.Add(P, Q)

		// output result
		PQ = toAffineG1(PQ)
		fmt.Print(PQ)

	} else if opindex == 2 {
		// g1 * ff

		// init variales
		a := new(ecc.Scalar)
		P := new(ecc.G1)
		aP := new(ecc.G1)

		// Set variable P
		g1_value := g(filename1)
		P.SetBytes(g1_value)

		// Set variable a
		ff_value := ff(filename2)
		a.SetString(ff_value)

		// Calculate aP = P * a
		aP.ScalarMult(a, P)

		// output result
		aP = toAffineG1(aP)
		fmt.Print(aP)

	} else if opindex == 3 {
		// g2 + g2
		P := new(ecc.G2)
		Q := new(ecc.G2)
		PQ := new(ecc.G2)

		// Set variable P
		g1_value1 := g(filename1)
		P.SetBytes(g1_value1)

		// Set variable Q
		g1_value2 := g(filename2)
		Q.SetBytes(g1_value2)

		// Calculate PQ = P + Q
		PQ.Add(P, Q)

		// output result
		PQ = toAffineG2(PQ)
		fmt.Print(PQ)

	} else if opindex == 4 {
		// g2 * ff

		// init variales
		a := new(ecc.Scalar)
		P := new(ecc.G2)
		aP := new(ecc.G2)

		// Set variable P
		g2_value := g(filename1)
		P.SetBytes(g2_value)

		// Set variable a
		ff_value := ff(filename2)
		a.SetString(ff_value)

		// Calculate aP = P * a
		aP.ScalarMult(a, P)

		// output result
		aP = toAffineG2(aP)
		fmt.Print(aP)

	} else if opindex == 5 {
		// ff + ff

		// init variales
		a := new(ecc.Scalar)
		b := new(ecc.Scalar)
		ab := new(ecc.Scalar)

		// Set variable a
		ff_value1 := ff(filename1)
		a.SetString(ff_value1)

		// Set variable a
		ff_value2 := ff(filename2)
		b.SetString(ff_value2)

		// Calculate ab = a + b
		ab.Add(a, b)

		// output result
		fmt.Print(ab)

	} else if opindex == 6 {
		// ff * ff

		// init variales
		a := new(ecc.Scalar)
		b := new(ecc.Scalar)
		ab := new(ecc.Scalar)

		// Set variable a
		ff_value1 := ff(filename1)
		a.SetString(ff_value1)

		// Set variable a
		ff_value2 := ff(filename2)
		b.SetString(ff_value2)

		// Calculate ab = a * b
		ab.Mul(a, b)

		// output result
		fmt.Print(ab)

	} else {
		fmt.Println("Invalid operation index")
	}

}
