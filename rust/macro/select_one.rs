// 下面是一些常见的 Rust宏选择器：
//
// item  ：条目，例如函数、结构、模块等
// block ：代码块
// stmt  ：语句
// pat   ：模式
// expr  ：表达式
// ty    ：类型
// ident ：标识符
// path  ：路径，例如 foo、 ::std::mem::replace, transmute::<_, int>, …
// meta  ：元信息条目，例如 #[…]和 #![rust macro…] 属性
// tt    ：词条树

macro_rules! select_one {
    ($type: ty, $var: ident, $condition: expr => $true: expr ; $false: expr) => {
        let $var: $type = if $condition { $true } else { $false };
    };
}

fn select_one_example() {
    let testvar: i32 = if 3 > 2 { 3 } else { 4 };

    println!("testvar is: {}", testvar);

    select_one!(i32, x, 3 > 2 => 3 ; 4);
    dbg!(x);
}

macro_rules! say_yo {
    ($name: expr) => {
        println!("Yo, {}", $name);
    };
}

fn say_yo_example() {
    say_yo!("Carl");
}

fn main() {
    println!(">>> select_one example:");
    select_one_example();
    println!(">>> say_yo example:");
    say_yo_example();
}
