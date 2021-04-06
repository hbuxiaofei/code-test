#![allow(improper_ctypes)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]

use std;

include!(concat!(std::env!("OUT_DIR"), "/rfb.rs"));

fn main() {
    println!("Hello, world!");

    unsafe {
		let mut arg_len = 0 as i32;
        let mut arg_ptr: *mut i8 = std::ptr::null_mut();

        let server = rfbGetScreen(&mut arg_len, &mut arg_ptr, 400, 300, 8, 3, 4);

        (*server).frameBuffer = malloc(400*300*4) as *mut i8;

        rfbInitServerWithPthreadsAndZRLE(server);
        rfbRunEventLoop(server, -1, 0);
    };
}

