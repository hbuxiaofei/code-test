use std::{
    time::Duration,
};
use yew::{html, Callback, Component, ComponentLink, Html, ShouldRender};
use yew::services::interval::{IntervalService, IntervalTask};
use yew::services::{ConsoleService, Task};
use wasm_bindgen::{JsCast, prelude::Closure};

use web_sys::{HtmlAudioElement, AudioBuffer, AudioBufferSourceNode, AudioContext, OfflineAudioContext};

use crate::common::msg::Msg;

const SOURCE_SOUND: &[u8] = include_bytes!("../content/sound/dog.mp3");

pub struct Body {
    link: ComponentLink<Self>,
    job: Option<Box<dyn Task>>,
    time: String,
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
            _standalone: (standalone_handle, clock_handle),
        }
    }

    fn update(&mut self, msg: Self::Message) -> ShouldRender {
        match msg {
            Msg::ButtonStart => {
                self.job = None;
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

                let show_str = format!("> SOURCE_SOUND len is: {:?}", SOURCE_SOUND.len());
                ConsoleService::info(&show_str);

                let array_u8 = js_sys::Uint8Array::new_with_length(SOURCE_SOUND.len() as u32);
                for i in 0..(SOURCE_SOUND.len()) {
                    array_u8.fill(SOURCE_SOUND[i], i as u32, (i+1) as u32);
                }

                let array_buf = array_u8.buffer();

                let audio_ctx =
                    OfflineAudioContext::new_with_number_of_channels_and_length_and_sample_rate(
                        1,
                        SOURCE_SOUND.len() as u32,
                        128000.0
                    ).unwrap();


                let song = audio_ctx.create_buffer_source().unwrap();
                let handler = move | buf: AudioBuffer | {
                    let buffer: Option<&AudioBuffer> = Some(&buf);

                    song.set_buffer(buffer);
                    // song.connect_with_audio_node(audio_ctx.destination().as_ref());
                    song.start();
                };

                // let handle = Box::new(handler) as Box<dyn FnMut(_)>;
                let handle = Box::new(handler) as Box<dyn FnMut(_)>;

                let cb = Closure::wrap(handle);

                // audio_ctx.decode_audio_data(&array_buf);
                audio_ctx.decode_audio_data_with_success_callback(&array_buf,
                    cb.as_ref().unchecked_ref());
                cb.forget();
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
                </div>
            </>
        }
    }
}
