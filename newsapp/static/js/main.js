function sortarticles(ele){
    document.getElementById('sort').value=ele.value
    document.getElementById('searchkeywordform').submit()
}
window.addEventListener("load", (event) => {
let menuBtn = document.querySelectorAll('li.adminlinks')
    menuBtn.forEach((li) => {
        li.addEventListener("click", (e) => {
            menuBtn.forEach((el) => 
            el.classList.remove("active"));
            li.classList.add("active");
            pages=JSON.stringify(li.classList.value)
            if(pages.includes('greetmessage')){
                document.getElementById('welcomemessage').style.display='block'
                document.getElementById('createuser').style.display='none'
            }else if(pages.includes('createuser')){
                document.getElementById('createuser').style.display='block'
                document.getElementById('welcomemessage').style.display='none'
            }
        });
    });
});
