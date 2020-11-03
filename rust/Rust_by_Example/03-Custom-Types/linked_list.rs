use crate::List::*;

enum List {
    // Cons: 元组结构体，包含一个元素和一个指向下一个节点的指针
    Cons(u32, Box<List>),
    // Nil: 尾节点，表明链表结束
    Nil,
}

impl List {
    // 创建一个空链表
    fn new() -> List {
        // `Nil` 为 `List` 类型
        Nil
    }

    // 处理一个列表，得到一个头部带上一个新元素的同样类型的列表并返回此值
    fn prepend(self, elem: u32) -> List {
        // `Cons`同样为 List 类型
        Cons(elem, Box::new(self))
    }

    // 返回列表的长度
    fn len(&self) -> u32 {
        match *self {
            Cons(_, ref tail) => 1 + tail.len(),
            Nil => 0,
        }
    }

    // 将列表以字符串的形式返回
    fn stringify(&self) -> String {
        match *self {
            Cons(head, ref tail) => format!("{}, {}", head, tail.stringify()),
            Nil => format!("Nil"),
        }
    }
}

fn main() {
    // 创建一个空链表
    let mut list = List::new();

    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);

    println!("linked list has length: {}", list.len());
    println!("{}", list.stringify());
}
