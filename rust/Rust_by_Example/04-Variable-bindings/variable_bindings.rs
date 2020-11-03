// Rust 通过静态类型确保类型安全。变量绑定可以在声明变量时标注类型。
// 不过在多数情况下，编译器能够从字面内容推导出变量的类型，大大减少了标注类型的负担。
//
//

fn main() {
    let an_integer = 1u32;
    println!("An integer: {:?}", an_integer);

    // 将 `an_integer` 复制到 `copied_integer`
    let copied_integer = an_integer;
    println!("An copied integer: {:?}", copied_integer);

    let a_boolean = true;
    println!("An boolean: {:?}", a_boolean);

    let unit = ();
    println!("Meet the unit value: {:?}", unit);

    // 编译器会对未使用变量产生警告，可在变量名前加 下划线 消除警告
    let _unused_variable = 2u32;
}
