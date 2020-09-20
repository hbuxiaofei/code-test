// ## 题目
//
// 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
//
// - 示例 1:
// 输入: "abcabcbb"
// 输出: 3
// 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
//
// - 示例 2:
// 输入: "bbbbb"
// 输出: 1
// 解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
//
// - 示例 3:
// 输入: "pwwkew"
// 输出: 3
// 解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
//      请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
//
//
// ## 思路
// 滑动窗口
//

struct Solution {}

impl Solution {
    pub fn length_of_longest_substring(s: String) -> i32 {
        let mut max = 0;
        let mut seq_tmp: Vec<char> = vec![];
        for (_, ch) in s.chars().enumerate() {
            if seq_tmp.contains(&ch) {
                while !seq_tmp.is_empty() {
                    if seq_tmp.remove(0) == ch {
                        break;
                    }
                }
            }
            seq_tmp.push(ch);
            if seq_tmp.len() > max {
                max = seq_tmp.len();
            }
        }
        max as i32
    }
}

fn main() {
    let test_str = String::from("abcabcbb");
    let result_ok = 3;
    let result = Solution::length_of_longest_substring(test_str);
    println!(
        "[length_of_longest_substring] Solution result: {:?}",
        result
    );
    assert_eq!(result, result_ok);

    let test_str = String::from("bbbbb");
    let result_ok = 1;
    let result = Solution::length_of_longest_substring(test_str);
    println!(
        "[length_of_longest_substring] Solution result: {:?}",
        result
    );
    assert_eq!(result, result_ok);

    let test_str = String::from("abcab12345");
    let result_ok = 8;
    let result = Solution::length_of_longest_substring(test_str);
    println!(
        "[length_of_longest_substring] Solution result: {:?}",
        result
    );
    assert_eq!(result, result_ok);

    let test_str = String::from("pwwkew");
    let result_ok = 3;
    let result = Solution::length_of_longest_substring(test_str);
    println!(
        "[length_of_longest_substring] Solution result: {:?}",
        result
    );
    assert_eq!(result, result_ok);
}
