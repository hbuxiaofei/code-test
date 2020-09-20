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

struct Solution {}

impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        let mut i = 0;
        let mut j = 0;

        let avg_len = (nums1.len() + nums2.len()) / 2;

        let mut left_num = 0;
        let mut right_num = 0;

        for _ in 0..avg_len + 1 {
            if i < nums1.len() && j < nums2.len() {
                if nums1[i] < nums2[j] {
                    right_num = left_num;
                    left_num = nums1[i];
                    i = i + 1;
                } else {
                    right_num = left_num;
                    left_num = nums2[j];
                    j = j + 1;
                }
            } else {
                if i >= nums1.len() {
                    right_num = left_num;
                    left_num = nums2[j];
                    j = j + 1;
                } else {
                    right_num = left_num;
                    left_num = nums1[i];
                    i = i + 1;
                }
            }
        }

        if (nums1.len() + nums2.len()) % 2 != 0 {
            return left_num as f64;
        }

        ((left_num + right_num) as f64) / (2 as f64)
    }
}

fn case1() {
    let nums1 = vec![1, 3];
    let nums2 = vec![2];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("ret = {}", ret);
    assert_eq!(2.0, ret);
}

fn case2() {
    let nums1 = vec![1, 2];
    let nums2 = vec![3, 4];

    let ret = Solution::find_median_sorted_arrays(nums1, nums2);
    println!("ret = {}", ret);
    assert_eq!(2.5, ret);
}

fn main() {
    case1();
    case2();
}
