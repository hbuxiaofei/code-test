#[macro_use]
extern crate error_chain;

mod errors {
    error_chain! {}
}
use errors::*;

quick_main!(run);

fn run() -> Result<()> {
    use std::env::args;
    use std::fs::File;
    use std::io::prelude::*;
    use std::io::BufReader;

    let file = args()
        .skip(1)
        .next()
        .ok_or(Error::from("filename needed"))?;

    ///////// 显式链化! ///////////
    let f = File::open(&file).chain_err(|| "unable to read the input file")?;

    for line in BufReader::new(f).lines() {
        let line = line.chain_err(|| "cannot read a line")?;
        println!("{}", line);
    }

    Ok(())
}

// instead by quick_main!(run);
fn main_bak() {
    if let Err(e) = run() {
        println!("error {}", e);

        /////// 查看错误链... ///////
        for e in e.iter().skip(1) {
            println!("caused by: {}", e);
        }

        std::process::exit(1);
    }
}
// $ cargo run foo
// error unable to read the damn file
// caused by: No such file or directory (os error 2)
