enum Person {
    // 一个 `enum` 可能是个 `unit-like` (类单元结构体)
    Engineer,
    Scientist,
    // 或像一个元组结构体
    Height(i32),
    Weight(i32),
    // 或像一个普通结构体
    Info { name: String, height: i32 },
}

// 此函数将一个 `Person` enum 作为参数，无返回值
fn inspect(p: Person) {
    match p {
        Person::Engineer => println!("Is enginner!"),
        Person::Scientist => println!("Is scientist!"),

        // 从 `enum` 内部解析 `i`
        Person::Height(i) => println!("Has a height of {}.", i),
        Person::Weight(i) => println!("Has a weight of {}.", i),

        // 将 `Info` 解析成 `name` 和 `height`
        Person::Info { name, height } => {
            println!("{} is {} tall!", name, height);
        }
    }
}

fn main() {
    let person = Person::Height(18);
    inspect(person);

    let amira = Person::Weight(10);
    inspect(amira);

    let dave = Person::Info {
        name: "Dave".to_owned(),
        height: 72,
    };
    inspect(dave);

    let rebecca = Person::Scientist;
    inspect(rebecca);

    let rohan = Person::Engineer;
    inspect(rohan);
}
