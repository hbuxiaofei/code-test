// ## 题目
// 给定两个大小为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。
//
// 请你找出这两个正序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
//
// 你可以假设 nums1 和 nums2 不会同时为空。
//
//
// - 示例 1:
// nums1 = [1, 3]
// nums2 = [2]
//
// 则中位数是 2.0
//
// - 示例 2:
// nums1 = [1, 2]
// nums2 = [3, 4]
//
// 则中位数是 (2 + 3)/2 = 2.5
//
// ## 思路：
//
// 利用二分查找和栈解决思路：
// 假设两个数组分别为：
// m = [23, 69, 180, 400, 500, 600, 800]
// n = [2 , 14, 36, 57, 99, 110]
//
// 1. 取m[0],n[0]较大的一个，即m[0] = 23;
//
// 2. 利用二分法在n中找出所有小于23的数，入栈 stack = [2, 14], 此时m, n分别为：
//  m = [23, 69, 180, 400, 500, 600, 800]
//  n = [36, 57, 99, 110]
//
// 3. 重复执行步骤1,2直到len(stack)长度不小于avg_len = (len(m)+len(n))/2
//
// 4. 结果即为stack[avg_len] 或者 (stack[stack-1] + stack[stack])/2
//

struct Solution {}

pub fn get_binary_insert_index(nums: &Vec<i32>, l: usize, r: usize,num: i32) -> usize {
    // 2   14   36   57   99   110
    //        ^
    //        23
    // index is 2

    let mut left_index = l;
    let mut right_index = r;

    if num <= nums[left_index] {
        left_index = if num == nums[left_index] { left_index + 1 } else { left_index };
        return left_index;
    }

    if num >= nums[right_index] {
        return right_index + 1;
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
    right_index
}


impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        let v1 = &nums1;
        let v2 = &nums2;

        let total_len = v1.len() + v2.len();
        let avg_len = total_len / 2;

        let mut index1 = 0;
        let mut index2 = 0;

        let mut stack = Vec::new();
        loop {
            if index1 >= v1.len() && index2 >= v2.len() {
                break
            }

            if index1 >= v1.len() {
                stack.push(v2[index2]);
                index2 = index2 + 1;
                continue
            }

            if index2 >= v2.len() {
                stack.push(v1[index1]);
                index1 = index1 + 1;
                continue
            }

            if v1[index1] > v2[index2] {
                let index_tmp = index2;
                index2 = get_binary_insert_index(v2, index2, v2.len() - 1, v1[index1]);
                for i in index_tmp..index2 {
                    stack.push(v2[i]);
                }
            } else {
                let index_tmp = index1;
                index1 = get_binary_insert_index(v1, index1, v1.len() - 1,v2[index2]);
                for i in index_tmp..index1 {
                    stack.push(v1[i]);
                }
            }

            if index1 + index2 > avg_len {
                break;
            }
        }

        if total_len % 2 == 1 {
            return stack[avg_len] as f64;
        }

        ((stack[avg_len - 1] + stack[avg_len]) as f64) / 2.0
    }
}

fn case1() {
    let nums1 = vec![1, 3];
    let nums2 = vec![2];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(2.0, ret);
}

fn case2() {
    let nums1 = vec![1, 2];
    let nums2 = vec![3, 4];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(2.5, ret);
}

fn case3() {
    let nums1 = vec![2, 14, 36, 57, 99, 110];
    let nums2 = vec![23, 69, 180, 400, 500, 600, 800];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(99.0, ret);
}

fn case4() {
    let nums1 = vec![0, 0];
    let nums2 = vec![0, 0];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(0.0, ret);
}

fn case5() {
    let nums1 = vec![];
    let nums2 = vec![1];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(1.0, ret);
}

fn case6() {
    let nums1 = vec![1,1,3,3];
    let nums2 = vec![1,1,3,3];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("[find_median_sorted_arrays] Solution result: {}", ret);
    assert_eq!(2.0, ret);
}
fn main() {
    case1();
    case2();
    case3();
    case4();
    case5();
    case6();
}
