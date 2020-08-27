struct Student {
    grade: String,
    class: String,
}


trait ShowClass {
    fn show_class(&self);
}
impl ShowClass for Student {
    fn show_class(&self) {
        println!("My class is: {}", self.class);
    }
}


trait ShowGrade {
    fn show_grade(&self);
}
impl ShowGrade for Student {
    fn show_grade(&self) {
        println!("My grade is: {}", self.grade);
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
        self.show_class();
        self.show_grade();
    }
}


fn main() {
    // let st = Student{class: String::from("class1")};
    // st.show_class();

    let st = Student{class: String::from("two"), grade: String::from("one")};
    st.show_property();

}
