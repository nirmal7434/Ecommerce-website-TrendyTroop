
        function openPopup(type) {
            document.getElementById("popup").style.display = "block";
            document.getElementById("overlay").style.display = "block";
            switchForm(type);


        }
        function closePopup() {
        function openPopup(type) {
            document.getElementById("popup").style.display = "block";
            document.getElementById("overlay").style.display = "block";
            switchForm(type);


        }
        function closePopup() {
            document.getElementById("popup").style.display = "none";
            document.getElementById("overlay").style.display = "none";
             let registerForm = document.getElementById("register-form");
             registerForm.querySelectorAll("input").forEach(input => input.value = "");
             document.querySelectorAll("#popup .error-text").forEach(div => div.innerText = "");

        }
        function switchForm(type) {
            if (type === 'login') {
                document.getElementById("login-form").style.display = "block";
                document.getElementById("register-form").style.display = "none";
            } else {
                document.getElementById("login-form").style.display = "none";
                document.getElementById("register-form").style.display = "block";
            }
        }
        function submitLogin() {
            alert("Login submitted: " + document.getElementById("login-username").value);
        }

    document.addEventListener("DOMContentLoaded", function () {
        let messagePopup = document.getElementById("messagePopup");  // Change this ID if your popup has a different one
        let messagesList = messagePopup?.querySelector(".messages"); // Adjust if your message container is different

        if (messagesList && messagesList.innerText.trim() !== "") {
            // Show the popup (Modify based on your popup structure)
            messagePopup.style.display = "block";

            // If using a modal, trigger it via JavaScript (Example for Bootstrap Modal)
            // $('#messagePopup').modal('show'); // Uncomment if using Bootstrap modal

            // Automatically hide the popup after 3 seconds
            setTimeout(() => {
                messagePopup.style.display = "none";
            }, 3000);
        }
    });
            document.getElementById("popup").style.display = "none";
            document.getElementById("overlay").style.display = "none";
             let registerForm = document.getElementById("register-form");
             registerForm.querySelectorAll("input").forEach(input => input.value = "");
             document.querySelectorAll("#popup .error-text").forEach(div => div.innerText = "");

        }
        function switchForm(type) {
            if (type === 'login') {
                document.getElementById("login-form").style.display = "block";
                document.getElementById("register-form").style.display = "none";
            } else {
                document.getElementById("login-form").style.display = "none";
                document.getElementById("register-form").style.display = "block";
            }
        }
        function submitLogin() {
            alert("Login submitted: " + document.getElementById("login-username").value);
        }

    document.addEventListener("DOMContentLoaded", function () {
        let messagePopup = document.getElementById("messagePopup");  // Change this ID if your popup has a different one
        let messagesList = messagePopup?.querySelector(".messages"); // Adjust if your message container is different

        if (messagesList && messagesList.innerText.trim() !== "") {
            // Show the popup (Modify based on your popup structure)
            messagePopup.style.display = "block";

            // If using a modal, trigger it via JavaScript (Example for Bootstrap Modal)
            // $('#messagePopup').modal('show'); // Uncomment if using Bootstrap modal

            // Automatically hide the popup after 3 seconds
            setTimeout(() => {
                messagePopup.style.display = "none";
            }, 3000);
        }
    });