// ---- define elements ----
let layer1 = document.getElementById("layer1");
let BtnSpeak_E = document.getElementById("BtnSpeak_E");
let BtnSubmit_E = document.getElementById("BtnSubmit_E");
let BtnAddToTest_E = document.getElementById("BtnAddToTest_E");
let InputGuess_E = document.getElementById("InputGuess_E");
let LblCorrectWordText_E = document.getElementById("LblCorrectWordText_E");
// ---- end of elements ----

function OnClickBtnSpeak_E(){
    LblCorrectWordText_E.innerHTML = pick_random_word_from_all_words();
}

function OnClickBtnSubmit_E(){

}

function OnClickBtnAddToTest_E(){

}