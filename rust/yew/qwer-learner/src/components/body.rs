use std::{
    time::Duration,
};
use yew::{html, Callback, Component, ComponentLink, Html, ShouldRender};
use yew::services::interval::{IntervalService, IntervalTask};
use yew::services::{ConsoleService, Task};

use web_sys::HtmlAudioElement;

use crate::common::msg::Msg;

pub struct Body {
    link: ComponentLink<Self>,
    job: Option<Box<dyn Task>>,
    time: String,
    messages: Vec<&'static str>,
    _standalone: (IntervalTask, IntervalTask),
}

impl Body {
    fn get_current_time() -> String {
        let date = js_sys::Date::new_0();
        String::from(date.to_locale_time_string("en-US"))
    }
}

impl Component for Body {
    type Message = Msg;
    type Properties = ();

    fn create(_props: Self::Properties, link: ComponentLink<Self>) -> Self {
        let standalone_handle = IntervalService::spawn(
            Duration::from_secs(60),
            // This callback doesn't send any message to a scope
            Callback::from(|_| {
                ConsoleService::info("> Standalone timer callback.");
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
            time: Body::get_current_time(),
            messages: Vec::new(),
            _standalone: (standalone_handle, clock_handle),
        }
    }

    fn update(&mut self, msg: Self::Message) -> ShouldRender {
        match msg {
            Msg::ButtonStart => {
                self.job = None;
                self.messages.push("Button [Start] pressed.");
                ConsoleService::info("> Button [Start] pressed.");

                let audio_url = "http://dict.youdao.com/dictvoice?type=0&audio=";
                let word = "start";
                let word_url =  audio_url.to_string() + &word.to_string();
                let result = HtmlAudioElement::new_with_src(word_url.as_str());
                match result {
                    Ok(v) => {
                        match v.play() {
                            Ok(_ok) => ConsoleService::info("> new html audio ok."),
                            Err(_err) => ConsoleService::warn("> play audio err."),
                        }
                    },
                    Err(_e) => ConsoleService::warn("> new html audio err."),
                }

                true
            }
            Msg::UpdateTime => {
                self.time = Body::get_current_time();
                true
            }
        }
    }

    fn change(&mut self, _props: Self::Properties) -> ShouldRender {
        false
    }

    fn view(&self) -> Html {
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
