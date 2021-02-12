use yew::{html, Bridge, Component, ComponentLink, Html, ShouldRender};
use yew::services::{ConsoleService};
use yew::agent::Bridged;

use crate::common::msg::Key;
use crate::common::event_bus::{EventBus};

pub struct Keyboard {
    inputs: String,
    _producer: Box<dyn Bridge<EventBus>>,
}

impl Component for Keyboard {
    type Message = Key;
    type Properties = ();

    fn create(_props: Self::Properties, link: ComponentLink<Self>) -> Self {
        Self {
            inputs: String::with_capacity(100),
            _producer: EventBus::bridge(link.callback(Key::SetText)),
        }
    }

    fn update(&mut self, msg: Self::Message) -> ShouldRender {
	match msg {
	    Key::SetText(text) => {
                let s = format!("> window key {} pressed.", text);
                ConsoleService::info(s.as_str());
	    }
	    Key::Submit => {
                ConsoleService::info("> window key [enter] pressed.");
	    }
	}

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

