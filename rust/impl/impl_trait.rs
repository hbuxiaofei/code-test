struct Example {
    number: i32,
}

trait Thingy {
    fn do_thingy(&self);
}
impl Thingy for Example {
    fn do_thingy(&self) {
        println!("doing a thing! also, number is {}!", self.number);
    }
}

trait Over {
    fn do_over(&self);
}
impl Over for Example {
    fn do_over(&self) {
        println!("doing a thing over ! also, number is {}!", self.number);
    }
}

fn main() {
    let ex = Example{number: 10};
    ex.do_thingy();
    ex.do_over();
}
