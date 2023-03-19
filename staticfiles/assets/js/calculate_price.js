function calculate(duration, percent, price) {
    var total = price + ((percent * price)/100)
    var monthly = total / duration
    monthly = monthly.toFixed(2)
    total = total + " UZS"
    monthly = monthly + " UZS"
    $("#div_main").show()
    $("#total").text(total)
    $("#monthly").text(monthly)
}