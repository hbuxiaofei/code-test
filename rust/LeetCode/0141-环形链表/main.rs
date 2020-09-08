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

use std::ptr;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ListNode {
    val: i32,
    next: *mut ListNode,
}

impl ListNode {
    pub fn new(val: i32) -> Self {
        let node = ListNode {
            val,
            next: ptr::null_mut(),
        };

        node
    }

    pub fn set_next(&mut self, new: *mut ListNode) -> &mut ListNode {
        unsafe {
            (*self).next = new;
            &mut *new
        }
    }

    pub fn get_next(&self) -> &mut ListNode {
        return unsafe { &mut *self.next };
    }

    pub fn as_ptr(&self) -> *mut ListNode {
        self as *const _ as *mut _
    }

    pub fn value(&self) -> &i32 {
        &self.val
    }
}

struct Solution {}

impl Solution {
    pub fn has_cycle(head: &mut ListNode) -> bool {
        let mut fast_p = &*head;
        let mut slow_p = &*head;

        while !fast_p.as_ptr().is_null() && !fast_p.get_next().as_ptr().is_null() {
            slow_p = slow_p.get_next();
            fast_p = fast_p.get_next().get_next();

            if slow_p.as_ptr() == fast_p.as_ptr() {
                return true;
            }
        }

        false
    }
}

fn show_list(head: &mut ListNode) {
    let mut n = head;
    let max = 10; // 最多显示10个节点，防止链表有环，形成死循环输出
    let mut i = 0;
    while n.as_ptr() != ptr::null_mut() {
        print!("{:?} ", n.value());
        n = n.get_next();

        i += 1;
        if i > max {
            break;
        }
    }
    print!("\n");
}

fn case_ok1() {
    let node1 = &mut ListNode::new(1);

    print!("[has_cycle] list: ");
    show_list(node1);

    let result = Solution::has_cycle(node1);
    println!("[has_cycle] Solution result: {:?}", result);
    assert_eq!(result, false);
}

fn case_ok2() {
    let node3 = &mut ListNode::new(3);
    let node2 = &mut ListNode::new(2);
    let node0 = &mut ListNode::new(0);
    let node_4 = &mut ListNode::new(-4);

    node3.set_next(node2); // node(3) -> node(2)
    node2.set_next(node0); // node(3) -> node(2) -> node(0)
    node0.set_next(node_4); // node(3) -> node(2) -> node(0) -> node(-4)

    print!("[has_cycle] list: ");
    show_list(node3);

    let result = Solution::has_cycle(node3);
    println!("[has_cycle] Solution result: {:?}", result);
    assert_eq!(result, false);
}

fn case_bad1() {
    let node3 = &mut ListNode::new(3);
    let node2 = &mut ListNode::new(2);
    let node0 = &mut ListNode::new(0);
    let node_4 = &mut ListNode::new(-4);

    node3.set_next(node2); // node(3) -> node(2)
    node2.set_next(node0); // node(3) -> node(2) -> node(0)
    node0.set_next(node_4); // node(3) -> node(2) -> node(0) -> node(-4)
    node_4.set_next(node2); // node(3) -> node(2) -> node(0) -> node(-4)
                            //              ^                     |
                            //              |                     |
                            //              +---------------------+

    print!("[has_cycle] list: ");
    show_list(node3);

    let result = Solution::has_cycle(node3);
    println!("[has_cycle] Solution result: {:?}", result);
    assert_eq!(result, true);
}

fn case_bad2() {
    let node1 = &mut ListNode::new(1);
    let node2 = &mut ListNode::new(2);

    node1.set_next(node2); // node(1) -> node(2)
    node2.set_next(node1); // node(1) -> node(2)
                           //   ^          |
                           //   |          |
                           //   +----------+

    print!("[has_cycle] list: ");
    show_list(node1);

    let result = Solution::has_cycle(node1);
    println!("[has_cycle] Solution result: {:?}", result);
    assert_eq!(result, true);
}

fn main() {
    case_ok1();
    case_ok2();
    case_bad1();
    case_bad2();
}
