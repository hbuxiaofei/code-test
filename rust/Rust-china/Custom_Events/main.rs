// Rust 实现 Custom Events
//
// 本文设计了一个比较巧妙的 Events 模式, 不由地让人想起 Qt的 signal.
// 下面是核心代码以及使用例子. 具体更多细节可以参阅原文.
//
// 来源:  Rust语言中文社区: 【Rust日报】2020-11-16 Rust 实现 Custom Events
// 原文链接：https://rossketeer.medium.com/custom-events-in-rust-c4e534b6b8cb

#[derive(Copy, Clone)]
struct Ctr { cur: usize }

impl Ctr {
    fn next(self) -> Ctr {
        Ctr { cur: self.cur + 1 }
    }
    fn start() -> Ctr {
        Ctr { cur: 0 }
    }
}

impl From<Ctr> for usize {
    fn from(ctr: Ctr) -> usize {
        ctr.cur
    }
}

trait Sig {
    type Data;
    type Receiver: Rec;

    fn emit(&self, data: Self::Data);
    fn conn(&mut self) -> Self::Receiver;
    fn disc(&mut self, i: usize);
}

trait Rec {
    type Data;

    fn on_emit(self, data: Self::Data);
    fn get_id(&self) -> usize;
}

macro_rules! def_signal {
    ($sig:ident, $rec:ident, $data:ty, $cls:expr) => {

        pub struct $sig {
            ctr: Ctr,
            recs: Vec<$rec>
        }

        #[derive(Copy, Clone)]
        pub struct $rec {
            id: usize
        }

        impl Sig for $sig {
            type Data = $data;
            type Receiver = $rec;
            fn emit(&self, data: Self::Data) {
                self.recs.iter().for_each(|r| r.on_emit(data));
            }

            fn conn(&mut self) -> Self::Receiver {
                let i: usize = self.nxt();
                let rec = $rec::new(i);
                self.recs.push(rec);
                rec
            }

            fn disc(&mut self, i: usize) {
                let u = self.recs
                    .iter()
                    .position(|r| r.id == i)
                    .unwrap();
                println!("Removing Signal R{}", i);
                self.recs.remove(u);
            }
        }

        impl Rec for $rec {
            type Data = $data;

            fn on_emit(self, data: Self::Data) {
                $cls(self, data);
            }

            fn get_id(&self) -> usize {
                self.id
            }
        }

        impl $rec {
            fn new(id: usize) -> Self {
                Self { id }
            }
        }

        impl $sig {
            fn nxt(&mut self) -> usize {
                self.ctr = self.ctr.next();
                self.ctr.into()
            }
            fn new() -> Self {
                $sig {
                    recs: Vec::new(),
                    ctr: Ctr::start()
                }
            }
        }
    }
}

#[derive(Copy,Clone)]
struct MySigData {
    num: i32
}

fn main() {
    def_signal!(
        MySig, MyRec, MySigData, |this: MyRec, data: MySigData| {
            println!("MySig receiver R{} - num: {}", this.id, data.num);
        }
    );

    let mut ms2 = MySig::new();
    let r1 = ms2.conn();
    let r2 = ms2.conn();
    ms2.emit(MySigData { num: 3 } );
    ms2.disc(r1.id);
    ms2.emit(MySigData { num: 9 } );
    ms2.disc(r2.id);
}

