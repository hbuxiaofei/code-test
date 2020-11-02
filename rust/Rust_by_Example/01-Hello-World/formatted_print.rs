// format! : 将格式化文本写到字符串(String)，字符串是返回值不是参数
// print!  : 与format!类似，但将文本输出到控制台。
// println!: 与print!类似，但输出结果追加一个换行符。

// ? -> Debug
// o –> Octal    // 8进制
// x –> LowerHex // 16进制
// X -> UpperHex
// p –> Pointer
// b –> Binary   // 二进制
// e -> LowerExp
// E -> UpperExp

fn main() {
    println!("My name is {0}, {1} {0}", "Bond", "James");

    // 特殊的格式实现可以在后面加上 `:` 符号。
    println!("{} of {:b} people know binary, the other half don't", 1, 2);

    // 你可以按指定宽度来右对齐文本。
    // 下面语句输出"     1"，5个空格后面连着1。
    println!("{number:>width$}", number = 1, width = 6);
    println!("{number:>width$}", number = 12345, width = 3);

    // 你可以对数字左边位数上补0。下面语句输出"000001"。
    println!("{number:>0width$}", number = 1, width = 6);

    // 创建一个包含` I32 `类型结构体(structure)。命名为 `Structure`。
    //
    // 编译器提供了 dead_code（死代码，无效代码）
    // 一般情况lint会对未使用的函数产生警告,可以加上属性来抑制这个 lint。
    // 类似的还有：
    // #[allow(unused_variables)]
    // #[allow(unused_imports)]
    #[allow(dead_code)]
    #[derive(Debug)]
    struct Structure(i32);
    println!("Print struct `{:?}`", Structure(3));
    println!("Print struct human `{:#?}`", Structure(3)); // 美化打印

    let pi = 3.141592;
    println!("Pi is {:.2}", pi);
}
