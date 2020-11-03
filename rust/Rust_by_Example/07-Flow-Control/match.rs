// Rust 通过 match 关键字来提供模式匹配，用法和 C 语言的的 switch 类似。
fn match_pattern() {
    let number = 13;
    println!("Tell me about {}", number);
    match number {
        // 匹配单个值
        1 => println!("One!"),
        // 匹配多个值
        2 | 3 | 5 | 7 | 11 => println!("This is a prime"),
        // 匹配一个闭区间范围
        13..=19 => println!("A teen"),
        // 处理其他情况
        _ => println!("Ain't special"),
    }

    let boolean = true;
    let binary = match boolean {
        false => 0,
        true => 1,
    };
    println!("{} -> {}", boolean, binary);
}

fn match_tuple() {
    let pair = (0, -2);
    println!("Tell me about {:?}", pair);

    // match 可以解构一个元组
    match pair {
        // 绑定到第二个元素
        (0, y) => println!("First is `0` and `y` is `{:?}`", y),
        (x, 0) => println!("`x` is `{:?}` and last is `0`", x),
        _ => println!("It doesn't matter what they are"),
    }
}

fn main() {
    match_pattern();
    match_tuple();
}
