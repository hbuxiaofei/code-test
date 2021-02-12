// From https://www.syntaxsuccess.com/viewarticle/experimenting-with-rust-and-webassembly
#![recursion_limit = "256"]

mod components;
mod common;

use yew::{html, Component, ComponentLink, Html, ShouldRender};
use crate::components::{
    header::Header,
    footer::Footer,
    body::Body,
    keyboard::Keyboard,
};

pub struct Model;

impl Component for Model {
    type Message = ();
    type Properties = ();

    fn create(_props: Self::Properties, _link: ComponentLink<Self>) -> Self {
        Self
    }

    fn update(&mut self, _msg: Self::Message) -> ShouldRender {
        true
    }

    fn change(&mut self, _props: Self::Properties) -> ShouldRender {
        false
    }

    fn view(&self) -> Html {
        html! {
            <>
                <header>
                    <Header/>
                </header>
                <div>
                    <Body/>
                    <Keyboard/>
                </div>
                <footer>
                    <Footer/>
                </footer>
            </>
        }
    }
}

fn main() {
    yew::start_app::<Model>();
}
