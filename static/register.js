function onclickedalert(){
    const name = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if(!name || !email || !password){
        alert("Please fill the empty fields")
    }
}