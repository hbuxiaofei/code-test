// Rust 程序（大部分）由一系列语句构成：
//

// Rust 有多种语句。最普遍的语句类型有两种：一种是绑定变量，另一种是表达式带上分号：
fn main1() {
    // 变量绑定
    let x = 2;
    // 表达式
    x;
    x + 1;
    15;
    println!("x is: {}", x);
}

// 代码块也是表达式，所以它们在赋值操作中可以充当右值（r-values）。
// 代码块中的最后一条 表达式将赋给左值（l-value）。
// 需要注意的是，如果代码块最后一条表达式结尾处有分号，那 么返回值将变成 ()
fn main2() {
    let x = 5u32;

    let y = {
        let x_squared = x * x;
        let x_cube = x_squared * x;

        // 将此表达式的值赋给 `y`
        x_cube + x_squared + x
    };

    let z = {
        // 分号结束了这个表达式，于是将 `()` 赋值给 `z`
        2 * x;
    };
    println!("x is {:?}", x);
    println!("y is {:?}", y);
    println!("z is {:?}", z);
}

fn main() {
    main1();
    main2();
}
