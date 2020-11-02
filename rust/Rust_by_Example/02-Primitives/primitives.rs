fn main() {
    // 变量可以声明类型
    let logical: bool = true;

    // 常规声明
    let a_float: f64 = 1.0;

    // 后缀声明
    let an_integer = 5i32;

    println!(
        "logical:{:?} float:{:?} integer:{:?}",
        logical, a_float, an_integer
    );

    // 自动推断类型
    let default_float = 3.0; // `f64`
    let default_integer = 7; // `i32`

    println!("float:{:?} integer:{:?}", default_float, default_integer);

    let mut mutable = 12; // 可变类型

    println!("mutable before: {:?}", mutable);

    // 报错，变量的类型不可改变
    // mutable = true;

    mutable = 20;
    println!("mutable after: {:?}", mutable);
}
