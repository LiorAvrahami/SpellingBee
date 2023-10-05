function ColorBackGroundAsFeedback(b_good_feedback) {
    old_bg = document.body.style.background
    if (b_good_feedback) {
        document.body.style.background = "green"
    } else {
        document.body.style.background = "red"
    }
    setTimeout(function () {
        document.body.style.background = old_bg;
    }, 300);
}