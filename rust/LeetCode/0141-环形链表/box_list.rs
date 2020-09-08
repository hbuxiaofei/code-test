// ## 环形链表
//
// 给定一个链表，判断链表中是否有环。
// 为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置
// （索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。
//
// - 示例 1
//
// 输入：head = [3,2,0,-4], pos = 1
// 输出：true
// 解释：链表中有一个环，其尾部连接到第二个节点。
//   +-----+        +-----+        +-----+        +-----+
//   |     |        |     |        |     |        |     |
//   |  3  |  --->  |  2  |  --->  |  0  |  --->  |  -4 |
//   |     |        |     |        |     |        |     |
//   +-----+        +-----+        +-----+        +-----+
//                     ^                              |
//                     |                              |
//                     +------------------------------+
//
// - 示例 2
//
// 输入：head = [1,2], pos = 0
// 输出：true
// 解释：链表中有一个环，其尾部连接到第一个节点。
//
// +-----+        +-----+
// |     |        |     |
// |  1  |  --->  |  2  |
// |     |        |     |
// +-----+        +-----+
//    ^              |
//    |              |
//    +--------------+
//
// - 示例 3
//
// 输入：head = [1], pos = -1
// 输出：false
// 解释：链表中没有环。
//
// +-----+
// |     |
// |  1  |
// |     |
// +-----+
//
// ## 思路
//
// 双指针法，我们设置两个指针从head开始遍历，规定两个指针的前进速度不一样，分别
// 称为快、慢指针，slow指针每次前进一个，fast指针每次前进两个节点。如果存在环的
// 话，fast指针速度更快，一定会追上slow指针。而如果fast指针没有追上slow指针，一
// 定是因为链表不存在环。
//

#[derive(Hash, Eq, PartialEq, Debug, Clone)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}

struct Solution {}

impl Solution {
    pub fn has_cycle(head: Option<Box<ListNode>>) -> bool {
        let mut fast_p = &head;
        let mut slow_p = &head;

        while fast_p.is_some() && fast_p.as_ref().unwrap().next.is_some() {
            slow_p = &slow_p.as_ref().unwrap().next;
            fast_p = &fast_p.as_ref().unwrap().next.as_ref().unwrap().next;

            if slow_p == fast_p {
                return true;
            }
        }
        false
    }
}

fn case_ok() {
    let mut node = ListNode::new(1);
    let mut list_input = ListNode::new(2);
    list_input.next = Some(Box::new(node));
    node = list_input;
    list_input = ListNode::new(3);
    list_input.next = Some(Box::new(node));

    let result = Solution::has_cycle(Some(Box::new(list_input)));
    println!("[has_cycle] Solution result: {:?}", result);
    assert_eq!(result, false);
}

fn main() {
    case_ok();
}
