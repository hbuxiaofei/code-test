use libc;
use std::os::raw::{c_int, c_char, c_void, c_ulong};
use std::os::unix::io::AsRawFd;

pub const O_RDONLY: c_int = libc::O_RDONLY;
pub const O_WRONLY: c_int = libc::O_WRONLY;
pub const O_RDWR: c_int = libc::O_RDWR;

pub type IoctlRequest = c_ulong;

pub fn open(path: *const c_char, oflag: c_int) -> c_int {
    unsafe {
        libc::open(path, oflag)
    }
}

pub fn read(fd: c_int, buf: *mut c_void, count: usize) -> isize {
	unsafe {
        libc::read(fd, buf, count)
	}
}

pub fn write(fd: c_int, buf: *const c_void, count: usize) -> isize {
	unsafe {
        libc::write(fd, buf, count)
	}
}

pub fn lseek(fd: c_int, offset: i64, whence: c_int) -> i64 {
	unsafe {
        libc::lseek(fd, offset, whence)
	}
}

pub fn close(fd: c_int) -> c_int {
    unsafe {
        libc::close(fd)
    }
}

/// Run an [`ioctl`](http://man7.org/linux/man-pages/man2/ioctl.2.html)
/// with an immutable reference.
///
/// # Arguments
///
/// * `fd`: an open file descriptor corresponding to the device on which
/// to call the ioctl.
/// * `req`: a device-dependent request code.
/// * `arg`: an immutable reference passed to ioctl.
///
/// # Safety
///
/// The caller should ensure to pass a valid file descriptor and have the
/// return value checked.
pub fn ioctl_with_ref<F: AsRawFd, T>(fd: &F, req: c_ulong, arg: &T) -> c_int {
    unsafe {
        libc::ioctl(
            fd.as_raw_fd(),
            req as IoctlRequest,
            arg as *const T as *const c_void,
        )
    }
}


/// Run an [`ioctl`](http://man7.org/linux/man-pages/man2/ioctl.2.html)
/// with a mutable reference.
///
/// # Arguments
///
/// * `fd`: an open file descriptor corresponding to the device on which
/// to call the ioctl.
/// * `req`: a device-dependent request code.
/// * `arg`: a mutable reference passed to ioctl.
///
/// # Safety
///
/// The caller should ensure to pass a valid file descriptor and have the
/// return value checked.
pub unsafe fn ioctl_with_mut_ref<F: AsRawFd, T>(fd: &F, req: c_ulong, arg: &mut T) -> c_int {
	libc::ioctl(
		fd.as_raw_fd(),
		req as IoctlRequest,
		arg as *mut T as *mut c_void,
	)
}

