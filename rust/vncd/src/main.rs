#![allow(dead_code)]

mod ioctl;
mod framebuffer;

use std::os::raw::{c_char, c_void};
use vncserver::*;

unsafe extern "C" fn rfb_kbd_cb(down: RfbBool, key_sym: RfbKeySym, cl: *mut RfbClientRec) {
    println!(">>> key_sym: {:?}", key_sym);
    let open_flags = ioctl::O_RDWR;
    let fd = ioctl::open("/dev/tty0\0".as_ptr() as *const c_char, open_flags);
    ioctl::write(fd, "ls\r\n".as_ptr() as *const c_void, 4);
    ioctl::close(fd);
}

fn main() {
    println!("Hello, world!");

    let open_flags = ioctl::O_RDONLY;
    let fd = ioctl::open("/dev/fb0\0".as_ptr() as *const c_char, open_flags);

    let mut fb_var_info = framebuffer::FbVarScreeninfo::default();
    let ret = unsafe {
        ioctl::ioctl_with_mut_ref(&fd, framebuffer::FBIOGET_VSCREENINFO as u64, &mut fb_var_info)
    };
    println!(">>> fb_var_info ioctl ret: {}", ret);
    // 一个像素多少位
    println!(">>> bits_per_pixel: {}", fb_var_info.bits_per_pixel);
	// x分辨率
	println!(">>> xres: {}", fb_var_info.xres);
	// y分辨率
	println!(">>> yres: {}", fb_var_info.yres);


    let mut fb_fix_info = framebuffer::FbFixScreeninfo::default();
    let ret = unsafe {
        ioctl::ioctl_with_mut_ref(&fd, framebuffer::FBIOGET_FSCREENINFO as u64, &mut fb_fix_info)
    };
    println!(">>> fb_fix_info ioctl ret: {}", ret);
    // 一行大小
    println!(">>> line_length: {}", fb_fix_info.line_length);


    let width = fb_var_info.xres as i32;
    let height = fb_var_info.yres as i32;
    let bytes_per_pixel = (fb_var_info.bits_per_pixel / 8) as i32;
    let mem_size = width*height*bytes_per_pixel;

    // rfb_get_screen(width: i32, height: i32, bits_per_sample: i32, samples_per_pixel: i32, bytes_per_pixel: i32)
    let server = rfb_get_screen(width, height, 8, 3, bytes_per_pixel);
    rfb_framebuffer_malloc(server, mem_size as u64);
    unsafe {
        (*server).alwaysShared = RFB_TRUE
    };
    rfb_kbd_add_event(server, std::option::Option::Some( rfb_kbd_cb  ));

    unsafe {
        ioctl::read(fd, (*server).frameBuffer as *mut c_void, mem_size as usize)
    };

    rfb_init_server(server);

    while rfb_is_active(server) == RFB_TRUE {
        ioctl::lseek(fd, 0, 0);
        unsafe {
            ioctl::read(fd, (*server).frameBuffer as *mut c_void, mem_size as usize)
        };

        rfb_mark_rect_as_modified(server, 0, 0, width, height);
        unsafe {
            rfb_process_events(server, ((*server).deferUpdateTime * 1000) as i64)
        };
    }

    ioctl::close(fd);

    // rfb_run_event_loop(server, -1, 0);
}

