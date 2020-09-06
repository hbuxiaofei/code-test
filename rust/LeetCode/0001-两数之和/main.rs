// ## 题目
//
// 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那
// 两个整数，并返回他们的数组下标。
//
// 你可以假设每种输入只会对应一个答案。但是不能重复利用这个数组中同样的元素。
//
// - 示例:
//
// 给定 nums = [2, 7, 11, 15], target = 9
//
// 因为 nums[0] + nums[1] = 2 + 7 = 9
// 所以返回 [0, 1]
//
//
// ## 思路
// - 思路1
// 采用hash结构求解
// - 思路2
// 利用双层循环求解
//

struct Solution();

impl Solution {
    pub fn two_sum(&self, nums: Vec<i32>, target: i32) -> Vec<i32> {
        // 定义一个长度是 2，每个数字都是 -1 的数组
        let mut rev = vec![-1i32; 2];

        for i in 0..nums.len() {
            let a = target - nums[i];
            for j in i + 1..nums.len() {
                if a == nums[j] {
                    rev[0] = i as i32;
                    rev[1] = j as i32;
                    return rev;
                }
            }
        }
        rev
    }
}

fn main() {
    let s = Solution {};

    let test_input = vec![2, 7, 11, 15];
    let test_val = 9;
    let result_ok = vec![0, 1];
    let result = s.two_sum(test_input, test_val);
    println!("[two_sum] Solution result: {:?}", result);
    assert_eq!(result, result_ok);
}
