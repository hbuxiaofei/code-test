#![no_std] // 不链接Rust标准库
#![no_main]  // 禁用所有Rust层级的入口点

extern crate rlibc;

use core::panic::PanicInfo;

// 这行代码定义了一个Rust模块，它的内容应当保存在src/vga_buffer.rs文件中。
// 使用2018版次（2018 edition）的Rust时，我们可以把模块的子模块（submodule）
// 文件直接保存到src/vga_buffer/文件夹下，与vga_buffer.rs文件共存，而无需创建一个mod.rs文件。
mod vga_buffer;

#[no_mangle] // 不重整函数名
pub extern "C" fn _start() -> ! {
    // 因为编译器会寻找一个名为`_start`的函数，所以这个函数就是入口点
    // 默认命名为`_start`

    println!("Hello World{}", "!");

    loop {}
}

/// 这个函数将在panic时被调用
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    loop {}
}
