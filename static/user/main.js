

var regEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/g;
var regPhone = /^\+?1?\d{9,15}$/g;   // Javascript reGex for Phone Number validation.
var regName = /\d+$/g; 

document.getElementById("register-btn").addEventListener("click", function (event) {
    event.preventDefault()
    formValidation(event)
});

const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
};

function formValidation(e){
    var name = document.forms.register.fullname;
    var email = document.forms.register.email;
    var phone = document.forms.register.phone_number;
    var password = document.forms.register.password;
    var confirm_password = document.forms.register.confirm_password;


    if (name.value === "" || regName.test(name.value)) {
        window.alert("Please enter your name properly.");
        name.focus();
        return false;
    }

    if (!validateEmail(email.value)){
        alert("Invalid email");
        email.focus();
        return false
    }
    if (password.value === "") {
        alert("Please enter your password");
        password.focus();
        return false;
    }
    if (password.value.length < 6) {
        alert("Password should be atleast 6 character long");
        password.focus();
        return false;

    }
    if(!(password.value === confirm_password.value)){
        alert("Password is not same");
        confirm_password.focus();
        return false;
    }
    if (phone.value == "" || !regPhone.test(phone.value)) {
        alert("Please enter valid phone number.");
        phone.focus();
        return false;
    }
    document.forms.register.submit()    
    return true;
}

let registerForm = document.getElementById("register-form");
let loginForm = document.getElementById("login-form");
let open_login = document.getElementById("open-login");
let open_register = document.getElementById("open_register");
let curon = document.getElementById("curton");





open_register.addEventListener("click",()=>{

    let tl = anime.timeline({
        easing: 'easeInQuad',
        duration: 800,
    })
    tl.pause()
    tl.add({
        targets: '#curton',
        top: "0px",
    }).add({
        targets: "#register-form",
        complete: function () {
            document.querySelector('#login-form').style.display = 'none';
        },
    }).add({
        targets: "#login-form",
        begin: function () {
            document.querySelector('#register-form').style.display = 'block';
            
        },
    }).add({
        targets: '#curton',
        top: "-110%",
    })

})

open_login.addEventListener("click", () => {

    let tl = anime.timeline({
        easing: 'easeInQuad',
        duration: 500,
    })
    tl.pause()
    tl.add({
        targets: '#curton',
        top: "0px",
    }).add({
        targets: "#register-form",
        complete: function () {
            document.querySelector('#register-form').style.display = 'none';
        },
    }).add({
        targets: "#login-form",
        begin: function () {
            document.querySelector('#login-form').style.display = 'block';
        },
    }).add({
        targets: '#curton',
        top: "-110%",
    })

})