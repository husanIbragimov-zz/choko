function calculate(duration, percent, price) {
    var total = price + ((percent * price)/100);
    var monthly = total / duration;
    monthly = new Intl.NumberFormat('de-DE').format(total);
    total = new Intl.NumberFormat('de-DE').format(total);
    total = total + " UZS";
    monthly = monthly + " UZS";
    $("#div_main").show();
    $("#total").text(total);
    $("#monthly").text(monthly);
}
