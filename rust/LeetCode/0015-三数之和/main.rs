// ## 题目
//
// 三数之和
//
//
// 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，
// 使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
//
// 注意：答案中不可以包含重复的三元组。
//
// ## 示例：
//
// ```
// 给定数组 nums = [-1, 0, 1, 2, -1, -4]，
//
// 满足要求的三元组集合为：
// [
//   [-1, 0, 1],
//   [-1, -1, 2]
// ]
// ```
//
//
// ## 思路
//
// 双指针法
//
// 1. 先排序
// 2. 再通过双指针查找
// - step1
//  [-4,    -1,    -1,     0,     1,     2]
//           ^      ^             ^
//           |      |             |
//          pos     p1            p2
// - step2
//  [-4,    -1,    -1,     0,     1,     2]
//           ^             ^      ^
//           |             |      |
//          pos            p1     p2
//
//

struct Solution {}

impl Solution {
    pub fn three_sum(nums: Vec<i32>) -> Vec<Vec<i32>> {
        let mut ret = vec![];
        if nums.len() < 3 {
            return ret;
        }

        let mut v = nums;
        v.sort();

        for i in 0..(v.len() - 2) {
            if i > 0 && v[i] == v[i - 1] {
                continue;
            }

            for p1 in (i + 1)..(v.len() - 1) {
                if p1 > i + 1 && v[p1] == v[p1 - 1] {
                    continue;
                }

                let target = 0 - v[i] - v[p1];
                let mut p2 = v.len() - 1;
                loop {
                    if v[p2] == target {
                        ret.push(vec![v[i], v[p1], v[p2]]);
                        break;
                    } else if v[p2] > target {
                        break;
                    }

                    p2 = p2 - 1;
                    if p2 < p1 + 1 {
                        break;
                    }
                }
            }
        }

        ret
    }
}

fn case1() {
    let nums = vec![-1, 0, 1, 2, -1, -4];
    let ret = Solution::three_sum(nums);
    println!("[three_sum] Solution result: {:?}", ret);
}

fn case2() {
    let nums = vec![0, 0, 0, 0];
    let ret = Solution::three_sum(nums);
    println!("[three_sum] Solution result: {:?}", ret);
}

fn main() {
    case1();
    case2();
}
