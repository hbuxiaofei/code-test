// 可变变量
// 变量绑定默认是不可变的，但加上 mut 修饰语后变量就可以改变。
//
//
fn main() {
    let mut mutable_binding = 1;
    println!("Before mutation: {}", mutable_binding);
    mutable_binding += 1;
    println!("After mutation: {}", mutable_binding);

    let _immutable_binding = 1;
    // _immutable_binding += 1; // 错误
}
