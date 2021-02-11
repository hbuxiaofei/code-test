// From https://www.syntaxsuccess.com/viewarticle/experimenting-with-rust-and-webassembly
#![recursion_limit = "256"]

use std::time::Duration;
use yew::{html, Callback, Component, ComponentLink, Html, ShouldRender};
use yew::services::interval::{IntervalService, IntervalTask};
use yew::services::{ConsoleService, Task, TimeoutService};

pub enum Msg {
    ButtonStart,
    UpdateTime,
}

pub struct Model {
    link: ComponentLink<Self>,
    job: Option<Box<dyn Task>>,
    time: String,
    messages: Vec<&'static str>,
    _standalone: (IntervalTask, IntervalTask),
}

impl Model {
    fn get_current_time() -> String {
        let date = js_sys::Date::new_0();
        String::from(date.to_locale_time_string("en-US"))
    }
}

impl Component for Model {
    type Message = Msg;
    type Properties = ();

    fn create(_props: Self::Properties, link: ComponentLink<Self>) -> Self {
        let standalone_handle = IntervalService::spawn(
            Duration::from_secs(10),
            // This callback doesn't send any message to a scope
            Callback::from(|_| {
                ConsoleService::info(">>> Standalone timer callback.");
            }),
        );

        let clock_handle = IntervalService::spawn(
            Duration::from_secs(1),
            // Timer callback
            link.callback(|_| Msg::UpdateTime),
        );

        Self {
            link,
            job: None,
            time: Model::get_current_time(),
            messages: Vec::new(),
            _standalone: (standalone_handle, clock_handle),
        }
    }

    fn update(&mut self, msg: Self::Message) -> ShouldRender {
        match msg {
            Msg::ButtonStart => {
                self.job = None;
                self.messages.push("Button [Start] pressed.");
                ConsoleService::warn(">>> Button [Start] pressed.");
                true
            }
            Msg::UpdateTime => {
                self.time = Model::get_current_time();
                true
            }
        }
    }

    fn change(&mut self, _props: Self::Properties) -> ShouldRender {
        false
    }

    fn view(&self) -> Html {
        let has_job = self.job.is_some();
        html! {
            <>
                <div id="buttons">
                    <button onclick=self.link.callback(|_| Msg::ButtonStart)>
                        { "Start" }
                    </button>
                </div>
                <div id="wrapper">
                    <div id="time">
                        { &self.time }
                    </div>
                    <div id="messages">
                        { for self.messages.iter().map(|message| html! { <p>{ message }</p> }) }
                    </div>
                </div>
            </>
        }
    }
}

fn main() {
    yew::start_app::<Model>();
}
