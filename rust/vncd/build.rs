extern crate bindgen;

use std::env;
use std::path::PathBuf;

fn bindgen_fb() {
    let header = format!("{}", "/usr/include/linux/fb.h");
    let bindings = bindgen::Builder::default()
        .header(header)
        .allowlist_type("fb_var_screeninfo")
        .allowlist_type("fb_fix_screeninfo")
        .allowlist_var("FBIOGET_VSCREENINFO")
        .allowlist_var("FBIOGET_FSCREENINFO")
        .generate()
        .expect("unable to generate fb bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out_path.join("fb.rs"))
        .expect("couldn't write fb bindings!");
}

fn main() {
    bindgen_fb();
}

