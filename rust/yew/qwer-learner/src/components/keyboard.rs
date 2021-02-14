use yew::{html, Bridge, Component, ComponentLink, Html, ShouldRender};
use yew::services::{ConsoleService};
use yew::agent::Bridged;
use web_sys::{HtmlAudioElement};

use crate::common::msg::Key;
use crate::common::event_bus::{EventBus};

static AUDIO_URL: &str = "http://dict.youdao.com/dictvoice?type=0&audio=";
const SOURCE_DICT: &str = include_str!("../content/dicts/CET6_T.json");

pub struct Keyboard {
    start_status: String,
    start_style: String,
    dict: serde_json::Value,
    nr_dict: usize,
    index: usize,
    inputs: String,
    _producer: Box<dyn Bridge<EventBus>>,
    link: ComponentLink<Self>,
}

impl Component for Keyboard {
    type Message = Key;
    type Properties = ();

    fn create(_props: Self::Properties, link: ComponentLink<Self>) -> Self {
        let index = 0;
        let dict: serde_json::Value = serde_json::from_str(SOURCE_DICT).unwrap();
        let nr_dict: usize = dict.as_array().unwrap().len();

        Self {
            dict: dict,
            nr_dict: nr_dict,
            index: index,
            inputs: String::with_capacity(100),
            start_status: String::from("Start"),
            start_style: String::from("background-color:#F5F5F5"),
            _producer: EventBus::bridge(link.callback(Key::SetText)),
            link,
        }
    }

    fn update(&mut self, msg: Self::Message) -> ShouldRender {
	match msg {
	    Key::SetText(text) => {
                if self.start_status == String::from("Pause") && text.len() == 1 {
                    let b = text.as_bytes()[0];
                    let c: char = b as char;
                    self.inputs.push(c);

                    let word = self.dict[self.index]["name"].as_str().unwrap();

                    let mut need_play = false;
                    if word.starts_with(&self.inputs) {
                        if word.len() == self.inputs.len() {
                            self.inputs.clear();
                            self.index = self.index + 1;
                            if self.index >= self.nr_dict {
                                self.index = 0;
                            }
                            need_play = true;

                        }
                    } else {
                        self.inputs.clear();
                    }

                    if need_play {
                        let word = self.dict[self.index]["name"].as_str().unwrap();
                        let word_url = AUDIO_URL.to_string() + &word.to_string();
                        let audio = HtmlAudioElement::new_with_src(word_url.as_str()).unwrap();
                        audio.play().unwrap();
                    }
                }

                let word = self.dict[self.index]["name"].as_str().unwrap();
                let s = format!("> window key:{} for:{} inputs:{}, dict len:{}.",
                    text, word, self.inputs, self.nr_dict);
                ConsoleService::info(s.as_str());
	    }
	    Key::Submit => {
                if self.start_status == String::from("Start") {
                    self.start_status = String::from("Pause");
                    self.start_style = String::from("background-color:#008f53");

                    let word = self.dict[self.index]["name"].as_str().unwrap();
                    let word_url = AUDIO_URL.to_string() + &word.to_string();
                    let audio = HtmlAudioElement::new_with_src(word_url.as_str()).unwrap();
                    audio.play().unwrap();
                } else {
                    self.start_status = String::from("Start");
                    self.start_style = String::from("background-color:#F5F5F5");
                }
                ConsoleService::info("> window key [enter] pressed.");
	    }
	}

        true
    }

    fn change(&mut self, _props: Self::Properties) -> ShouldRender {
        false
    }

     fn view(&self) -> Html {
         let word = self.dict.get(self.index).unwrap();
         let word_name: &str = word["name"].as_str().unwrap();
         let word_trans: &str = word["trans"][0].as_str().unwrap();
         let name_byte = word_name.as_bytes();
         let inputs_byte = self.inputs.as_bytes();
         let name_byte_last = &name_byte[inputs_byte.len()..name_byte.len()];

         html! {
             <>
                <div id="buttons">
                    <button onclick=self.link.callback(|_| Key::Submit) style=self.start_style>
                        { &self.start_status }
                    </button>
                </div>
                 <div id="word">
                    { for inputs_byte.iter().map(|b| html! { <font color="red">{ *b as char }</font> }) }
                    { for name_byte_last.iter().map(|b| html! { <font color="white">{ *b as char }</font> }) }
                 </div>
                 <div id="trans">
                    <p> { &word_trans } </p>
                 </div>
             </>
         }
     }
}

