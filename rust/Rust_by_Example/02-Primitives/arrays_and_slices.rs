use std::mem;

fn analyze_slize(slice: &[i32]) {
    println!("first element of the slice: {}", slice[0]);
    println!("the slice has {} elements", slice.len());
}

fn main() {
    // 固定大小的数组
    let xs: [i32; 5] = [1, 2, 3, 4, 5];
    println!("first element of the array: {}", xs[0]);
    println!("second element of the array: {}", xs[1]);
    println!("array xs size: {}", xs.len());

    // 所有元素初始化成相同的值
    let ys: [i32; 10] = [0; 10];
    println!("ys is: {:?}", ys);

    // 数组是在堆中分配
    println!("ayyay occupies {} bytes", mem::size_of_val(&xs));

    // 切片（Slice）是对数据值的部分引用。
    println!("borrow the whole array as a slice");
    analyze_slize(&xs);

    println!("borrow a section of the array as a slice");
    analyze_slize(&ys[1..4]);

    let mut s = String::from("hello");
    s.push_str(" world");
    let slice1 = &s[0..6];
    let slice2 = &s[6..11];
    // s.push_str("!");  // s 被部分引用，禁止更改其值。
    println!("slice1 = {}", slice1);
    println!("slice2 = {}", slice2);
}
