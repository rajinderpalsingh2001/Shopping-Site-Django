$(document).ready(function () {
    $("#checkoutForm").validate();
});


$(document).ready(function () {
    $("#placeOrder").click(function (e) {
        var paymentmethod = $("input[name=paymentmethod]:checked").val();
        if (paymentmethod == "Online") {
            if ($("#checkoutForm").valid()) {
                e.preventDefault();
                var amount = document.getElementById('grandTotalwer').value * 100;
                // alert(amount);
                var options = {
                    "key": "rzp_test_dRWiKHS7zr2Gki",
                    "amount": amount,
                    "name": "",
                    "description": "",
                    "image": "",
                    "handler": function (response) {
                        //alert(response.razorpay_payment_id);
                        if (response.razorpay_payment_id == "") {
                            //alert('Failed');
                            window.location.href = "add_payment_details.php?status=failed";
                        } else {
                            var controls = document.getElementById("checkoutForm").elements;
                            var formdata = new FormData();
                            for (var i = 0; i < controls.length; i++) {
                                if (controls[i].type == "file") {
                                    formdata.append(controls[i].name, controls[i].files[0]);
                                } else {
                                    formdata.append(controls[i].name, controls[i].value);
                                }
                            }
                            var httpreg = new XMLHttpRequest();
                            httpreg.onreadystatechange = function () {
                                if (this.status == 200 && this.readyState == 4) {
                                    var output = this.responseText;
                                    console.log(output);
                                    window.location.href = "thanks.php?q=" + output;
                                }

                            };
                            httpreg.open("POST", "insertPayment.php", true);
                            httpreg.send(formdata);
                        }
                    },
                    "prefill": {
                        "name": "",
                        "email": document.getElementById("emailid").value,
                        'contact':document.getElementById("mobile").value
                    },
                    "notes": {
                        "address": ""
                    },
                    "theme": {
                        "color": "#F37254"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        }
    })
});


function addToCart(productid, qty = null) {
    if (qty == null) {
        if ($("#myFormQty").valid()) {
            var qtyval = document.getElementById("qty").value;
        } else {
            alert("Please choose the Quantity less than stock");
        }
    } else {
        qtyval = 'index';
    }
    if (qtyval != undefined) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (this.status == 200 && this.readyState == 4) {
                alert("1 Item added Successfully in the Cart");
                document.getElementById("cartCount").innerHTML = this.responseText;

            }
        };
        xmlhttp.open("GET", "addtoCart.php?q=" + productid + "&qty=" + qtyval, true);
        xmlhttp.send();
    }
}

function changeQty(productid, type, stock) {
    var quantity = parseInt(document.getElementById("quantity-" + productid).value);
    var flag;
    if (type == 'plus') {
        if (quantity >= stock) {
            document.getElementById("plusicon-" + productid).className = "fa fa-plus disabled";
            flag = 0;
        } else {
            document.getElementById("minusicon-" + productid).className = "fa fa-minus";
            document.getElementById("plusicon-" + productid).className = "fa fa-plus";
            quantity += 1;
        }
    } else if (type == 'minus') {
        if (quantity > 1) {
            quantity -= 1;
            document.getElementById("minusicon-" + productid).className = "fa fa-minus";
        } else {
            document.getElementById("minusicon-" + productid).className = "fa fa-minus disabled";
            flag = 0;
        }
    }
    if (flag != 0) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (this.status == 200 && this.readyState == 4) {
                var output = (JSON.parse(this.responseText));
                console.log(output);
                document.getElementById("quantity-" + productid).value = output.qty;
                document.getElementById("netprice-" + productid).innerHTML = output.netPrice;
                document.getElementById("grandTotal").innerHTML = output.grandTotal;
            }
        };
        xmlhttp.open("GET", "changeQty.php?q=" + productid + "&qty=" + quantity, true);
        xmlhttp.send();
    }
}
