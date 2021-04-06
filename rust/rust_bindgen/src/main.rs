include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

use std::env;


unsafe fn call_hello_from_c(){
    hello_from_c();
}


fn main() {
    println!("Hello, world!");
    unsafe {
        call_hello_from_c();
    }
}

