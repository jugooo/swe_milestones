console.log("Entered Javascript file");
const button_id = document.getElementById('button_main');

button_id.addEventListener('click',() => {
    console.log("Button Clicked");
    button_id.innerText = "Clicked";
});