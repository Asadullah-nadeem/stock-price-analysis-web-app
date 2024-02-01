// script.js

document.addEventListener("DOMContentLoaded", function() {
    // JavaScript animations or interactions can be added here
    // Example: Change background color on button click
    document.getElementById("submitBtn").addEventListener("click", function() {
        document.body.style.backgroundColor = getRandomColor();
    });

    function getRandomColor() {
        var letters = "0123456789ABCDEF";
        var color = "#";
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});
