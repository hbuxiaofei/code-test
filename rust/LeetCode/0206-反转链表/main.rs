// ## 题目
//
// 反转一个单链表 如输入: 1->2->3->4->5->NULL；输出: 5->4->3->2->1->NULL
//
//
// ## 思路
//
// 遍历链表，将元素的next的指针指向前一个元素
//

#[derive(PartialEq, Eq, Clone, Debug)]
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
    pub fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
        let mut lhs = head;
        let mut rhs = None;

        while let Some(mut node) = lhs {
            lhs = node.next.take();
            node.next = rhs;
            rhs = Some(node);
        }

        rhs
    }
}

fn main() {
    // 头插链表
    let mut node = ListNode::new(1);
    let mut list_input = ListNode::new(2);
    list_input.next = Some(Box::new(node));
    node = list_input;
    list_input = ListNode::new(3);
    list_input.next = Some(Box::new(node));

    if let Some(r) = Solution::reverse_list(Some(Box::new(list_input))) {
        println!("[reverse_list] Solution result: {:?}", r);
    }
}
