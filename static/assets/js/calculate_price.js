function calculate(duration, percent, price) {
    var total = price + ((percent * price)/100)
    var monthly = total / duration
    monthly = new Intl.NumberFormat('en-IN').format(total)
    total = new Intl.NumberFormat('en-IN').format(total);
    total = total + " UZS"
    monthly = monthly + " UZS"
    $("#div_main").show()
    $("#total").text(total)
    $("#monthly").text(monthly)
}