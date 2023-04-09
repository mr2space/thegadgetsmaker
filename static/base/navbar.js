
let menu = document.getElementById("menu");
let close = document.getElementById("close-sidebar");
let sidebar = document.getElementById("sidebar");



function closemsg(){
document.getElementById("msg-box").classList.add("deactive");
}

function closeAction(e){
    sidebar.classList.remove("active");
}

function openAction(e){
    sidebar.classList.add("active");
}

close.addEventListener("click",closeAction);
menu.addEventListener("click",openAction);


