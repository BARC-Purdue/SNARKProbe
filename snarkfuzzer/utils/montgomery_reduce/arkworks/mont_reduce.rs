#![allow(unused_imports)]
#![allow(unused_variables)]

extern crate pairing;
use pairing::{PrimeField};
use std::env;

fn main(){
    use pairing::bls12_381::{Fr, Fq};

    let tmp1 = Fr::from_str("0").unwrap();
    let tmp2 = Fq::from_str("0").unwrap();

    let args: Vec<String> = env::args().collect();
    
    if args.len() == 5 {
        print!("{}", tmp1);
    } else if args.len() == 7 {
        print!("{}", tmp2);
    }
}
