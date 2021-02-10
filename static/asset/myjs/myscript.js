function showSubcategory(str) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("output").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "getSubcategories.php?q=" + str, true);
    xmlhttp.send();
}


function showsubcat(str) {
    // alert();
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("subcategory").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "getSubCategorySelect.php?q=" + str, true);
    xmlhttp.send();
}


function show_product(str) {

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // alert(this.responseText);
            document.getElementById("productdiv").innerHTML = this.responseText;
        }
    };
    if (str == '') {
        xmlhttp.open("GET", "getproduct.php", true);
    } else {
        xmlhttp.open("GET", "getproduct.php?q=" + str, true);
    }
    xmlhttp.send();
}