// type 语句可以给一个已存在类型起一个新的名字。
// 类型必须要有 CamelCase（驼峰方式）的名称，
// 否则编译器会产生一个警告。对规则为例外的是基本类型： usize，f32等等。
//
//

// `NanoSecond` 是 `u64` 的新名字
type NanoSecond = u64;
type Inch = u64;

// 使用一个non_camel_case_types属性来忽略警告
#[allow(non_camel_case_types)]
type u64_t = u64;

fn main() {
    let nanoseconds: NanoSecond = 5 as u64_t;
    let inches: Inch = 2 as u64_t;

    println!("{} + {} = {} ?", nanoseconds, inches, nanoseconds + inches);
}
