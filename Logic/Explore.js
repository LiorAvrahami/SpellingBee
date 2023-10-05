// ---- define elements ----
let _Explore_Tab = document.getElementById("_Explore_Tab");
let BtnSpeak_E = document.getElementById("BtnSpeak_E");
let BtnSubmit_E = document.getElementById("BtnSubmit_E");
let BtnAddToTest_E = document.getElementById("BtnAddToTest_E");
let BtnSkip_E = document.getElementById("BtnSkip_E");
let InputGuess_E = document.getElementById("InputGuess_E");
let LblCorrectWordText_E = document.getElementById("LblCorrectWordText_E");
// ---- end of elements ----

let explore_word = "None"

function On_Explore_Tab_Open() {
    SelectNewWord();
}

function OnClickBtnSpeak_E() {
    speak(explore_word);
}

function OnClickBtnSubmit_E() {
    input_val = InputGuess_E.value
    if (CheckIfWordsAreEqual(input_val, explore_word)) {
        ColorBackGroundAsFeedback(true);
    } else {
        ColorBackGroundAsFeedback(false);
    }

}

function OnClickBtnAddToTest_E() {

}
function OnClickBtnSkip_E() {
    SelectNewWord();
}

function SelectNewWord() { explore_word = pick_random_word_from_all_words(); }