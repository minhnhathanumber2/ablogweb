document.getElementById("password_show").onclick = () =>{
    if (document.getElementById("password_input").type === "text"){
        document.getElementById("password_input").type="password";
        document.getElementById("password_show").innerText = "visibility"
    }
    else{
        document.getElementById("password_input").type = "text";
        document.getElementById("password_show").innerText = "visibility_off"
    }
}
document.getElementById("confirm_password_show").onclick = () =>{
    if (document.getElementById("confirm_password_input").type === "text"){
        document.getElementById("confirm_password_input").type="password";
        document.getElementById("confirm_password_show").innerText = "visibility"
    }
    else{
        document.getElementById("confirm_password_input").type = "text";
        document.getElementById("confirm_password_show").innerText = "visibility_off"
    }
}