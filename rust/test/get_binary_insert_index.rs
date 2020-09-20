
pub fn get_binary_insert_index(nums: Vec<i32>, num: i32) -> i32 {
    // 2   14   36   57   99   110
    //        ^
    //        23
    // index is 2

    let mut left_index = 0;
    let mut right_index = nums.len() - 1;

    if num <= nums[left_index] {
        left_index = if num == nums[left_index] { left_index + 1 } else { left_index };
        return left_index as i32;
    }

    if num >= nums[right_index] {
        return (right_index + 1) as i32;
    }

    let mut half_index = (left_index + right_index) / 2;
    loop {
        if nums[half_index] >= num {
            right_index = half_index;
        } else {
            left_index = half_index;
        }

        if ((right_index - left_index) as i32) <= 1 {
            break;
        }

        half_index = (left_index + right_index) / 2;
    }
    right_index as i32
}

fn case1() {
    let v = vec![2, 14, 36, 57, 99, 110];
    let ret = get_binary_insert_index(v, 23);
    println!("case1 ret is: {}", ret);
    assert_eq!(ret, 2);
}

fn case2() {
    let v = vec![2, 14, 36, 57, 99, 110];
    let ret = get_binary_insert_index(v, 2);
    println!("case2 ret is: {}", ret);
    assert_eq!(ret, 1);
}

fn case3() {
    let v = vec![10, 14, 36, 57, 99, 110];
    let ret = get_binary_insert_index(v, 2);
    println!("case3 ret is: {}", ret);
    assert_eq!(ret, 0);
}

fn case4() {
    let v = vec![10, 14, 36, 57, 99, 110];
    let ret = get_binary_insert_index(v, 120);
    println!("case4 ret is: {}", ret);
    assert_eq!(ret, 6);
}

fn case5() {
    let v = vec![10, 14, 36, 57, 99, 110];
    let ret = get_binary_insert_index(v, 110);
    println!("case5 ret is: {}", ret);
    assert_eq!(ret, 6);
}

fn case6() {
    let v = vec![10, 12, 14, 36, 57, 99, 110, 111, 113 ,114];
    let ret = get_binary_insert_index(v, 12);
    println!("case6 ret is: {}", ret);
    assert_eq!(ret, 1);
}

fn case7() {
    let v = vec![10, 12, 14, 36, 57, 99, 110, 111, 113 ,114];
    let ret = get_binary_insert_index(v, 111);
    println!("case7 ret is: {}", ret);
    assert_eq!(ret, 7);
}

fn main() {
    case1();
    case2();
    case3();
    case4();
    case5();
    case6();
    case7();
}
