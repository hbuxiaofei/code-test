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

fn test1() {
    let root = Some(Box::new(ListNode::new(100)));
    if let Some(n) = &root {
        println!("root is: {}", n.val);
    }
}

fn test2() {
    let root = Some(Box::new(ListNode::new(200)));
    let curr = &root;
    if let Some(n) = curr {
        println!("curr is: {}", n.val);
    }
}

fn test3() {
    let root = Some(Box::new(ListNode::new(300)));
    let root1 = &root;
    let root2 = &root1;
    let curr = &root2;
    if let Some(n) = curr {
        println!("curr is: {}", n.val);
    }
}

fn main() {
    test1();
    test2();
    test3();
}
