function datewise() {
    // alert();
    var from = document.getElementById("fromdate").value;
    var to = document.getElementById("todate").value;
    var status = document.getElementById("status").value;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            $("#accordion").accordion();
            console.log(this.responseText);
            document.getElementById("datewiseorder").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "vieworderdatewiseaction.php?q=" + from + "&r=" + to+"&s="+status, true);
    xmlhttp.send();
}