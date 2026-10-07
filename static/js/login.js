

const username = document.getElementById("username");

const password = document.getElementById("password");

// enter ở username sẽ chuyển sang password

username.addEventListener("keydown", function(event)
{
    if(event.key === "Enter")
    {
        event.preventDefault();

        password.focus();
    }
});

// ẩn hiện mật khẩu

function togglePassword(id) {

    let input = document.getElementById(id);

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}


