# rinux (A Rust Kernel)

This repository contains the source code for the rinux.

References:
[blog_os](https://github.com/phil-opp/blog_os)


## Requires
To create a bootable disk image from the compiled kernel, you need to install the [`bootimage`] tool:
```
rustup component add rust-src
rustup component add llvm-tools-preview
cargo install cargo-xbuild
cargo install bootimage
```


## Building
```
rustup default nightly
cargo xbuild --target x86_64-rinux.json
cargo build
cargo bootimage
```

## Running
You can run the disk image in [QEMU] through:
```
cargo run
```

You can also write the image to an USB stick for booting it on a real machine. On Linux, the command for this is:
```
dd if=target/x86_64-rinux/debug/bootimage-rinux.bin of=/dev/sdX && sync
```
