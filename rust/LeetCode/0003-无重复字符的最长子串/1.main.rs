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
// 采用双指针方法操作比较简单：
// 1. 定义一个保存最大长度变量max,两个移动的变量i,j和另外一个保存不重复字符串的
// 变量seq_tmp
// 2. 对给定的字符串s进行遍历，然后判断seq_tmp是否包含当前的字符，如果不包含
// 则j++,同时把当前的字符拼接到seq_tmp中，如果包含则i++,把当前循环的变量j重新
// 赋值为i,把当前保存的seq_tmp=""
// 3. 把max中的值与seq_tmp的长度进行比较，如果len(seq_tmp)>max则：max=len(seq_tmp)
// 4. 返回 max值即为所求
//

struct Solution();

impl Solution {
    pub fn length_of_logest_substring(&self, s: String) -> i32 {
        let seq: Vec<char> = s.chars().collect();
        let mut max = 0;
        for i in 0..seq.len() {
            let mut seq_tmp: Vec<char> = vec![];
            for j in i..seq.len() {
                if self.index_str(seq[j], seq_tmp.clone()) == -1 {
                    seq_tmp.push(seq[j]);
                    if seq_tmp.len() > max {
                        max = seq_tmp.len();
                    }
                } else {
                    break;
                }
            }
        }
        max as i32
    }

    fn index_str(&self, c: char, vec: Vec<char>) -> i32 {
        for i in 0..vec.len() {
            if vec[i] == c {
                return i as i32;
            }
        }
        -1
    }
}

fn main() {
    let s = Solution {};

    let test_str = String::from("abcabcbb");
    let result_ok = 3;
    let result = s.length_of_logest_substring(test_str);
    println!("[length_of_logest_substring] Solution result: {:?}", result);
    assert_eq!(result, result_ok);

    let test_str = String::from("bbbbb");
    let result_ok = 1;
    let result = s.length_of_logest_substring(test_str);
    println!("[length_of_logest_substring] Solution result: {:?}", result);
    assert_eq!(result, result_ok);

    let test_str = String::from("pwwkew");
    let result_ok = 3;
    let result = s.length_of_logest_substring(test_str);
    println!("[length_of_logest_substring] Solution result: {:?}", result);
    assert_eq!(result, result_ok);

    let test_str = String::from("abcab12345");
    let result_ok = 8;
    let result = s.length_of_logest_substring(test_str);
    println!("[length_of_logest_substring] Solution result: {:?}", result);
    assert_eq!(result, result_ok);
}
