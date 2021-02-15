/// 单纯Rust语言上考虑。
/// 我们在不同情况下解释&的意思：
/// 1. 在表达式上，表示的是借用。
/// 2 .在变量绑定上，表示解地址操作。
/// 3. 在类型声明上，表示引用类型。
///
/// ref的通用解释是:
/// 1. 在表达式上，无效关键字。
/// 2. 在模式匹配上，表示引用类型。

fn borrow_example1()  {
    let x: u32 = 100;

    // 可以同时又多个 "不可变" 借用
    let y: &u32 = &x;
    let z: &u32 = &x;
    let m: &u32 = &x;

    // ok
    println!("x:{}, y:{}, z:{}, m:{}", x, y, z, m );
}

fn borrow_example2()  {
    // 源变量x可变性
    let mut x: u32 = 100;

    // y是一个可变借用
    let y: &mut u32 = &mut x;

    *y = 101;
    println!("y:{}", y);
    println!("x:{}", x);
}

fn borrow_example3()  {
    let x: u32 = 100;
    let ref y: u32;

    y = &x;

    println!("y:{}", y);
    println!("x:{}", x);
}

fn main() {
    println!("\n> borrow_example1 run:");
    borrow_example1();
    println!("\n> borrow_example2 run:");
    borrow_example2();
    println!("\n> borrow_example3 run:");
    borrow_example3();
}
