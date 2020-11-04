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

// 需要 `allow` 来消除警告，因为只是用了一个变量
#[allow(dead_code)]
enum Color {
    // 这三者仅由它们的名字来表示
    Red,
    Blue,
    Green,

    // 这些元组含有类似的 `u32` 元素，分别对应不同的名字：颜色模型（color models）
    RGB(u32, u32, u32),
    HSV(u32, u32, u32),
    HSL(u32, u32, u32),
    CMY(u32, u32, u32),
    CMYK(u32, u32, u32, u32),
}

fn match_enum() {
    let color = Color::RGB(122, 17, 40);

    println!("What color is it?");

    match color {
        Color::Red => println!("The color is Red!"),
        Color::Blue => println!("The color is Blue!"),
        Color::Green => println!("The color is Green!"),
        Color::RGB(r, g, b) => println!("Red:{}, green:{}, and blue:{}", r, g, b),
        Color::HSV(h, s, v) => println!("Hue:{}, saturation:{}, value:{}", h, s, v),
        Color::HSL(h, s, l) => println!("Hue:{}, saturation:{}, lightness:{}", h, s, l),
        Color::CMY(c, m, y) => println!("Cyan:{}, magenta:{}, yellow:{}", c, m, y),
        Color::CMYK(c, m, y, k) => {
            println!("Cyan:{}, magenta:{}, yellow:{}, key(black): {}", c, m, y, k)
        } // 不需要其他分支，因为所有的情形都已经覆盖
    }
}

fn main() {
    match_pattern();
    match_tuple();
    match_enum();
}
