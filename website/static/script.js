function toggleWeightForm() {
    const weightForm = document.getElementById("weightForm");
    const overlay = document.querySelector(".popup-overlay");

    if (weightForm.style.display === "none" || weightForm.style.display === "") {
        weightForm.style.display = "block";
        overlay.style.display = "block";
    } else {
        weightForm.style.display = "none";
        overlay.style.display = "none";
    }
}


document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.getElementById("dateInput");


    // Set the initial date value to today if no value is provided
    if (!dateInput.value) {
        const today = new Date();
        dateInput.value = today.toISOString().split('T')[0];
    }

});
