const username = document.getElementById("username");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");
const phone = document.getElementById("phone");
const submitBtn = document.getElementById("submit"); // nếu có nút submit

// enter ở username sẽ chuyển sang password

username.addEventListener("keydown", function(event)
{
    if(event.key === "Enter")
    {
        event.preventDefault();

        password.focus();
    }
});

password.addEventListener("keydown", function(event)
{
    if(event.key === "Enter")
    {
        event.preventDefault();

        confirmPassword.focus();
    }
});

confirmPassword.addEventListener("keydown", function(event)
{
    if(event.key === "Enter")
    {
        event.preventDefault();

        phone.focus();
    }
});


 
// ẩn hiện mật khẩu

function togglePassword(id) {
let input = document.getElementById(id);

    if (input.type === "password") 
    {
        input.type = "text";
    } 
    else 
    {
        input.type = "password";
    }
}
    
// kiểm tra confirm password

const password = document.getElementById("password");
const confirm = document.getElementById("confirm_password");

confirm.addEventListener("input", function () {
    if (password.value !== confirm.value) {
        confirm.style.border = "2px solid red";
    } else {
        confirm.style.border = "2px solid green";
    }
});