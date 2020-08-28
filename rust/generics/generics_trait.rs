// 定义结构体
struct Student {
    grade: String,
    class: String,
}
// 结构体方法实现
impl Student {
    // 使用new方法创建结构体
    // fn new(grade: String, class: String) -> Student {
    fn new(grade: String, class: String) -> Self {  // 返回值Student可用Self代替
        Student {
            grade: grade,
            class: class,
        }
    }

    fn show(&self) {
        println!("1> My grade is: {}", self.grade);
        println!("1> My class is: {}", self.class);
    }
}


trait ShowClass {
    fn show_class(&self);
}
impl ShowClass for Student {
    fn show_class(&self) {
        println!("2> My class is: {}", self.class);
    }
}


trait ShowGrade {
    fn show_grade(&self);
}
impl ShowGrade for Student {
    fn show_grade(&self) {
        println!("2> My grade is: {}", self.grade);
    }
}


trait ShowProperty {
    fn show_property(&self);
}
// impl<T: ShowClass + ShowGrade> ShowProperty for T {
impl<T> ShowProperty for T
    where T:ShowClass + ShowGrade
{
    fn show_property(&self) {
        self.show_grade();
        self.show_class();
    }
}


fn main() {
    // let st = Student{class: String::from("class1")};
    // st.show_class();

    let st = Student::new(String::from("grade2"),
                          String::from("class1"));
    st.show();

    println!("");

    st.show_property();
}
