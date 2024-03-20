 function updateRange() {
    var rangeInput = document.getElementById('yearRange');
    var rangeValueSpan = document.getElementById('rangeValue');
    var rangeValues = rangeInput.value.split(",");
    var minValue = rangeValues[0];
    var maxValue = rangeValues[1];
    rangeValueSpan.textContent = minValue + ' - ' + maxValue;