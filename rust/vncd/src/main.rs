#![allow(dead_code)]

mod ioctl;
mod framebuffer;

use std::os::raw::{c_char};
use vncserver::*;

fn main() {
    println!("Hello, world!");

    let open_flags = ioctl::O_RDONLY;
    let fd = ioctl::open("/dev/fb0\0".as_ptr() as *const c_char, open_flags);

    let fb_fix_info = framebuffer::FbFixScreeninfo.default();

    let ret = ioctl::ioctl_with_mut_ref(&fd, framebuffer::FBIOGET_FSCREENINFO as u64, &mut fb_fix_info) ;
    println!(">>>>> ioctl ret: {}", ret);


    ioctl::close(fd);

    let server = rfb_get_screen(400, 300, 8, 3, 4);
    rfb_framebuffer_malloc(server, 400*300*4);
    rfb_init_server(server);
    rfb_run_event_loop(server, -1, 0);
}

