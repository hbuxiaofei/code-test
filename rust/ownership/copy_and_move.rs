// 常用的具有 copy trait 的有：
//
// 1. 所有整数类型，比如 u32。
// 2. 所有浮点数类型，比如 f64。
// 3. 布尔类型，bool，它的值是 true 和 false。
// 4. 字符类型，char。
// 5. 元组，当且仅当其包含的类型也都是 Copy 的时候。比如，(i32, i32) 是 Copy 的，但 (i32, String) 就不是。

fn main() {
    let a_char = '1';
    let a_tuple = (1, 2, 3);

    let a_string = String::from("hello world");
    let a_vec = vec![1, 2, 3];

    {
        let _b_char = a_char; // char copy
        let _b_tuple = a_tuple; // tuple copy

        let _b_string = a_string; // stirng move
        let _b_vec = a_vec; // vec move
    }

    println!("a_char = {:?}", a_char);
    println!("a_tuple = {:?}", a_tuple);

    // println!("a_vec = {:?}", a_vec);
    // println!("a_string = {:?}", a_string);
}
