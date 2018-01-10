function isNumeric(valueElement, messageElement){
    var value = document.getElementById(valueElement).value;
    if (!(!isNaN(parseFloat(value)) && isFinite(value))){
        document.getElementById('searchButton').disabled = true;
        document.getElementById(messageElement).innerHTML = "Please enter a valid number";
    }else{
        document.getElementById('searchButton').disabled = false;
        document.getElementById(messageElement).innerHTML = "";
    }
}

function advancedSearch(){
    var elem = document.getElementById('min-price');
    var button = document.getElementById('adv-search')
    if (elem.style.display == 'inline') {
        elem.style.display = 'none';
        button.value = 'Advanced Search'
            }
    else {
        elem.style.display = 'inline';
        button.value = 'Simple Search';
    }
}
