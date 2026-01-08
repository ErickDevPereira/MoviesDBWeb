const MSG = document.getElementById('going_on');
const BACK_BUTTON = document.getElementById('go_login');
let permission = true;

BACK_BUTTON.onclick = function() {
    if (permission) {
        timer = 3;
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                            MSG.innerText = `Going to Login in ${timer} sec`;
                            timer--;
                            if (timer === -1) {
                                //window.location.href returns the current URL as string, but when we assign it to something, we navigate to the new URL.
                                window.location.href = '/login'
                            }
                        }, i*1000)
        }
    }
    permission = false;
}