function showpassword() {
    var form = new FormData();
    var x = document.getElementById("password");
    var y = document.getElementById("conpassword");
    if (x.type === "password" || y.type === "password") {
        x.type = "text";
        y.type = "text";
        $("#eyeslash").removeClass("fa-eye-slash");
        $("#eyeslash").addClass("fa-eye");
    } else {
        x.type = "password";
        y.type = "password";
        $("#eyeslash").removeClass("fa-eye");
        $("#eyeslash").addClass("fa-eye-slash");

    }
}
function showpassword1() {
    var form = new FormData();
    var x = document.getElementById("password");
    var y = document.getElementById("conpassword");
    if (x.type === "password") {
        x.type = "text";
        // y.type = "text";
        $("#eyeslash").removeClass("fa-eye-slash");
        $("#eyeslash").addClass("fa-eye");
    } else {
        x.type = "password";
        // y.type = "password";
        $("#eyeslash").removeClass("fa-eye");
        $("#eyeslash").addClass("fa-eye-slash");

    }
}


