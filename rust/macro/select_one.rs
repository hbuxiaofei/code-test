
macro_rules! select_one {
    ($type: ty, $var: ident, $condition: expr => $true: expr ; $false: expr) => {
        let $var: $type = if $condition {
            $true
        } else {
            $false
        };
    }
}

fn main() {
    let testvar : i32 = if 3 > 2 {
        3
    } else {
        4
    };

    println!("testvar is: {}", testvar);

    select_one!(i32, x, 3 > 2 => 3 ; 4);
    dbg!(x);
}
