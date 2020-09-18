#![no_std]
#![no_main]
#![feature(custom_test_frameworks)]
#![test_runner(rinux::test_runner)]
#![reexport_test_harness_main = "test_main"]

use rinux::println;
use core::panic::PanicInfo;

#[no_mangle]
pub extern "C" fn _start() -> ! {
    println!("Hello World{}", "!");

    rinux::init();

    #[cfg(test)]
    test_main();

    println!("It did not crash!");
    rinux::hlt_loop();
}

/// This function is called on panic.
#[cfg(not(test))]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    rinux::hlt_loop();
}

#[cfg(test)]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    rinux::test_panic_handler(info)
}

#[test_case]
fn trivial_assertion() {
    assert_eq!(1, 1);
}
