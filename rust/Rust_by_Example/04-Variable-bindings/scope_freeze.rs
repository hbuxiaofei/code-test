fn main() {
    // 此绑定存在于main函数中
    let long_lived_binding = 1;
    {
        // 这是一个代码块，比main函数拥有一个更小的作用域
        // 此绑定只存在于本代码块
        let short_lived_binding = 2;
        println!("inner short: {}", short_lived_binding);
        // 此绑定*隐藏*(覆盖)了外面的绑定
        let long_lived_binding = 5_f32;
        println!("inner long: {}", long_lived_binding);
    } // 代码块结束

    // 报错！`short_lived_binding` 在此作用域上不存在
    // println!("outer short: {}", short_lived_binding);

    println!("outer long: {}", long_lived_binding);

    // 此绑定同样*隐藏*(覆盖)了前面的绑定
    let long_lived_binding = 'a';
    println!("outer long: {}", long_lived_binding);

    let mut _mutable_integer = 7i32;
    {
        // 重新声明一个同名的_mutable_integer
        let _mutable_integer = _mutable_integer;
        // _mutable_integer = 50; // 重新声明的_mutable_integer未被mut修饰
        println!("mutable freeze integer is: {}", _mutable_integer);
    }
    _mutable_integer = 3;
    println!("mutable integer is: {}", _mutable_integer);
}
