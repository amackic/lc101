function isNumeric(valueElement, messageElement){
    debugger;
    var value = document.getElementById(valueElement).value;
    if (!(!isNaN(parseFloat(value)) && isFinite(value))){
        document.getElementById('searchButton').disabled = true;
        document.getElementById(messageElement).innerHTML = "Please enter a valid number";
    }else{
        document.getElementById('searchButton').disabled = false;
        document.getElementById(messageElement).innerHTML = "";
    }
}
