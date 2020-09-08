// ## 题目
//
// 给出两个*非空*的链表用来表示两个非负的整数。其中，它们各自的位数是按照*逆序*
// 的方式存储的，并且它们的每个节点只能存储*一位*数字。
// 如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
// 您可以假设除了数字 0 之外，这两个数都不会以 0 开头。
//
// ### 示例：
//
// - 输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
// - 输出：7 -> 0 -> 8
// - 原因：342 + 465 = 807
//
// ## 思路
//

// Definition for singly-linked list.
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
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        let mut dummy1 = l1;
        let mut dummy2 = l2;
        let mut root = Some(Box::new(ListNode::new(0)));
        let mut curr = &mut root;
        let mut carry = 0;

        while dummy1.is_some() || dummy2.is_some() {
            match curr {
                Some(inner_node) => {
                    let first = dummy1.take().unwrap_or(Box::new(ListNode::new(0)));
                    let second = dummy2.take().unwrap_or(Box::new(ListNode::new(0)));
                    let mut sum = first.val + second.val + carry;
                    carry = sum / 10;
                    sum = sum % 10;
                    inner_node.next.get_or_insert(Box::new(ListNode::new(sum)));
                    curr = &mut inner_node.next;
                    dummy1 = first.next;
                    dummy2 = second.next;
                }
                None => break,
            }
        }

        if carry == 1 {
            if let Some(node) = curr {
                node.next.get_or_insert(Box::new(ListNode::new(1)));
            }
        }

        root.unwrap().next
    }
}

fn main() {
    let mut node = ListNode::new(1);
    let mut list1 = ListNode::new(2);
    list1.next = Some(Box::new(node));
    node = list1;
    list1 = ListNode::new(3);
    list1.next = Some(Box::new(node));

    node = ListNode::new(3);
    let mut list2 = ListNode::new(2);
    list2.next = Some(Box::new(node));
    node = list2;
    list2 = ListNode::new(1);
    list2.next = Some(Box::new(node));

    println!("[has_cycle] Solution result: {:?}", list1);
    println!("[has_cycle] Solution result: {:?}", list2);

    let result = Solution::add_two_numbers(Some(Box::new(list1)), Some(Box::new(list2)));

    println!("[has_cycle] Solution result: {:?}", result);
}
