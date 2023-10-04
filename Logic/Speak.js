function getVoices() {
    let voices = speechSynthesis.getVoices();
    if (!voices.length) {
        // some time the voice will not be initialized so we can call spaek with empty string
        // this will initialize the voices 
        let utterance = new SpeechSynthesisUtterance("");
        speechSynthesis.speak(utterance);
        voices = speechSynthesis.getVoices();
    }
    return voices;
}

async function speak(text_to_speak) {
    // create a SpeechSynthesisUtterance to configure the how text to be spoken 
    let speakData = new SpeechSynthesisUtterance();
    speakData.volume = 1; // From 0 to 1
    speakData.rate = 0.5; // From 0.1 to 10
    speakData.pitch = 1; // From 0 to 2
    speakData.text = text_to_speak;
    speakData.lang = 'en';
    speakData.voice = getVoices()[0];

    // pass the SpeechSynthesisUtterance to speechSynthesis.speak to start speaking 
    speechSynthesis.speak(speakData);
}