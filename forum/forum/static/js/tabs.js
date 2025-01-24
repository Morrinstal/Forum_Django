document.addEventListener("DOMContentLoaded", function () {
    const loginTab = document.getElementById("login-tab");
    const signupTab = document.getElementById("signup-tab");
    const loginPane = document.getElementById("login");
    const signupPane = document.getElementById("signup");
    const tabs = document.querySelectorAll('.nav-link');
    const indicator = document.querySelector('.tab-indicator');


    loginTab.addEventListener("click", function () {
        loginPane.classList.add("show", "active");
        signupPane.classList.remove("show", "active");
    });

    signupTab.addEventListener("click", function () {
        signupPane.classList.add("show", "active");
        loginPane.classList.remove("show", "active");
    });


    function updateIndicator(){
        const activaTab = document.querySelector('.nav-link.active');
        const rect = activaTab.getBoundingClientRect();
        const parentRect = activaTab.parentElement.getBoundingClientRect();
        indicator.style.width = `${rect.width}px`;
        indicator.style.left = `${rect.left - parentRect.left}px`;
    }

    tabs.forEach((tab)=>{
        tab.addEventListener('click',function(){
            tabs.forEach((t)=> t.classList.remove('active'));
            this.classList.add('active');
            updateIndicator();
        });
    });
    updateIndicator();
});