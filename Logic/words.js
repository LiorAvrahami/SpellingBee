let word_dictionary = null;
let user_test_word_pool = null

async function load_all() {
  load_all_words();
  load_user_test_words();
}

async function load_all_words() {
    if(word_dictionary == null){
    file_name = "dictionary\\word_dictionary.json";
    let x = await fetch(file_name);
    let y = await x.text();
    word_dictionary = JSON.parse(y);
    }
}

async function load_user_test_words(){

}

// inclusive exclusive
function getRandom(max) {
  return Math.floor(Math.random() * max);
}

function pick_random_word_from_all_words(){
  keys = Object.keys(word_dictionary);
  idx = getRandom(keys.length);
  return word_dictionary[keys[idx]]["word"];
}
  
load_all();