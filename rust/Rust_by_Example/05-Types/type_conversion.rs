// Rust 在基本类型之间没有提供隐式类型转换（强制类型转换）
// 使用 as 关键字进行显式类型转换
//
// 一般来说，Rust 的整型类型的转换规则遵循 C 语言的惯例，除了那些在 C 语言是未定义行为的情况。
// 在 Rust 中，所有的整型类型转换的行为都得到了很好的定义。
//

// 消除会溢出的类型转换的所有警告
#![allow(overflowing_literals)]

use std::convert::From;
use std::convert::TryFrom;
use std::convert::TryInto;
use std::fmt;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

fn from_and_into() {
    let my_str = "hello";
    let my_string = String::from(my_str);

    println!("my string is: {}", my_string);

    let num = Number::from(30);
    println!("My number is {:?}", num);

    let int = 5;
    let num2: Number = int.into();
    println!("My number2 is {:?}", num2);
}

#[derive(Debug, PartialEq)]
struct EvenNumber(i32);

impl TryFrom<i32> for EvenNumber {
    type Error = ();

    fn try_from(value: i32) -> Result<Self, Self::Error> {
        if value % 2 == 0 {
            Ok(EvenNumber(value))
        } else {
            Err(())
        }
    }
}

fn try_from_and_into() {
    // TryFrom
    assert_eq!(EvenNumber::try_from(8), Ok(EvenNumber(8)));
    assert_eq!(EvenNumber::try_from(5), Err(()));

    // TryInto
    let result: Result<EvenNumber, ()> = 8i32.try_into();
    assert_eq!(result, Ok(EvenNumber(8)));
    let result: Result<EvenNumber, ()> = 5i32.try_into();
    assert_eq!(result, Err(()));
}

struct Circle {
    radius: i32,
}

impl fmt::Display for Circle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Circle of radius {}", self.radius)
    }
}

fn to_and_from_string() {
    let circle = Circle { radius: 6 };
    println!("circle: {}", circle.to_string());
    println!("circle: {}", circle);

    let parsed: i32 = "5".parse().unwrap();
    let turbo_parsed = "10".parse::<i32>().unwrap();
    let sum = parsed + turbo_parsed;
    println!("sum: {:?}", sum);
}

fn main() {
    let decimal = 65.4321_f32;

    // 报错！不能隐式的转换类型
    // let integer: u8 = decimal;

    // 正确。显式转换类型
    let integer: u8 = decimal as u8;
    let character = integer as char;
    println!("Casting: {} -> {} -> {}", decimal, integer, character);

    // 在计算机底层会截取数字的低8位（the least significant bit，LSB）
    // 0011_1110_1000 低八位： 1110_1000 = 232
    println!("1000 as a u8 is : {}", 1000 as u8);

    from_and_into();
    try_from_and_into();
    to_and_from_string();
}
