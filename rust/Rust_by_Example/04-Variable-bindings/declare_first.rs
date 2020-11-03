fn main() {
    // 声明一个变量绑定
    let a_binding;
    {
        let x = 2;

        // 初始化这个绑定
        a_binding = x * x;
    }
    println!("a binding: {:?}", a_binding);
}
