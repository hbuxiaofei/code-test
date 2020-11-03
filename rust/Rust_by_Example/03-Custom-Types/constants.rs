// Rust 有两种常量，可以在任意作用域声明，包括全局作用域。这两种常量都要显式地标注：
//
// const： 不可改变的值（常用类型）。
// static： 在 'static 生命周期内可能发生改变的变量。
//

static LANGUAGE: &'static str = "Rust";
const THRESHOLD: i32 = 10;
static mut NUMBER: i32 = 5;

fn is_big(n: i32) -> bool {
    // 在一般函数中访问常量
    n > THRESHOLD
}

fn main() {
    println!("LANGUAGE is {}", LANGUAGE);

    // 在main主函数中访问常量
    println!("The threshold is {}", THRESHOLD);
    let n = 16;
    println!("{} is {}", n, if is_big(n) { "big" } else { "small" });

    unsafe {
        NUMBER += 1;
        println!("NUMBER is {}", NUMBER);
    }
}
