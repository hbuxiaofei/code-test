// 单行注释，注释内容直到行尾
/* 块注释，注释内容一直到结束分隔符 */


/// 对接下来的项生成帮助文档。
///! 对封闭项生成帮助文档。

fn main() {
    let x = 5 + /* 90 + */ 5;
    println!("Is `x` 10 or 100? x = {}", x);
}
