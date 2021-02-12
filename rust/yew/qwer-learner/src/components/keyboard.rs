use yew::{html, Component, ComponentLink, Html, ShouldRender};
use yew::services::{ConsoleService};
use wasm_bindgen::{JsCast, prelude::Closure};

pub struct Keyboard;

impl Component for Keyboard {
    type Message = ();
    type Properties = ();

    fn create(_props: Self::Properties, _link: ComponentLink<Self>) -> Self {
	let window = web_sys::window().unwrap();

	let cb = Closure::wrap(Box::new(|| {
	    ConsoleService::info("> key [someone] pressed.");
	}) as Box<dyn FnMut()>);

	window.add_event_listener_with_callback("keydown",
            cb.as_ref().unchecked_ref()).unwrap();
	cb.forget();

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
             <></>
         }
     }
}

