function onclickedalert(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if(!email || !password){
        alert("Please fill the empty fields")
    }
}