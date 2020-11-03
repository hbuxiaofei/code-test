// literal 字面量
//
// 数字字面量可以加上类型标记作为后缀来标注类型。
// 举个例子，要指定字面量 42 为 i32 类型，可以写成 42i32。
//
// 未加上后缀的数字字面量的类型视使用它们的情况而定。
// 如果没有限定，编译器会将整型定为 i32 类型，
// 将浮点数定为 f64 类型。
//
fn main() {
    // 有后缀的字面量，它们的类型在初始化的时候就确定
    let x = 1u8;
    println!("size of `x` in bytes: {}", std::mem::size_of_val(&x));

    let y = 2u32;
    println!("size of `y` in bytes: {}", std::mem::size_of_val(&y));

    let z = 3f32;
    println!("size of `z` in bytes: {}", std::mem::size_of_val(&z));

    let i = 1;
    println!("size of `i` in bytes: {}", std::mem::size_of_val(&i));

    let f = 1.0;
    println!("size of `f` in bytes: {}", std::mem::size_of_val(&f));
}
