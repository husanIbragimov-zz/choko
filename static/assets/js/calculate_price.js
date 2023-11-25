var total;
var monthly;
var image_total;
var image_monthly;


function calculate(duration, percent, price, status, id) {
    // const { duration, percent, price, status, id } = duration
    console.log(duration, percent, price, status, id)
    console.log(Math.ceil((((duration.percent / 100)*duration.price)+duration.price)/duration.duration), "<---")
    console.log(Math.ceil((((duration.percent / 100)*duration.price)+duration.price)/duration.duration), (((duration.percent / 100)*duration.price)+duration.price)/duration.duration)
    let new_price = Math.trunc(((((duration.percent / 100)*duration.price)+duration.price)/duration.duration).toFixed(0)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
    $('#monthly').text(new_price)
    // if (status === "images") {
    //     type_data.image = {
    //         id: id, price: price, temp_price: price,
    //     }
    //     if (type_data.variant === 0) {
    //         image_total = price + ((percent * price) / 100);
    //         image_monthly = image_total / duration;
    //         image_monthly = Math.trunc(image_monthly);
    //         type_data.image.temp_price = Math.trunc(image_total).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
    //         type_data.image.price = price

    //     } else {
    //         image_total = price + ((type_data.variant.percent * price) / 100);
    //         image_monthly = image_total / type_data.variant.duration;
    //         image_monthly = Math.trunc(image_monthly);
    //         type_data.image.temp_price = Math.trunc(image_total).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
    //         type_data.image.price = price
    //     }
    //     image_monthly = Math.trunc(image_monthly).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    //     image_monthly = image_monthly + " uzs/oy";
    //     price = type_data.image.temp_price + " uzs";
    //     $("#monthly").text(image_monthly);
    //     $("#origin_price").text(price);
    // } else {
    //     type_data.variant = {
    //         id: duration.id, duration: duration.duration, percent: duration.percent
    //     }

    //     if (type_data.image === 0) {
    //         total = parseFloat(duration.price) + ((duration.percent * parseFloat(duration.price)) / 100);
    //         monthly = total / duration.duration;
    //         monthly = monthly.toFixed(2);
    //         price = Math.trunc(total).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " uzs";
    //     } else {
    //         total = parseFloat(type_data.image.price) + ((duration.percent * parseFloat(type_data.image.price)) / 100);
    //         monthly = total / duration.duration;
    //         monthly = Math.trunc(monthly);
    //         price = Math.trunc(total).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " uzs";
    //     }
    //     monthly = Math.trunc(monthly).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    //     monthly = monthly + " uzs/oy";

    //     $("#monthly").text(monthly);
    //     $("#origin_price").text(price);
    // }
}

// ================================================ Banner Deadline ====================================================
// Function to pad numbers with leading zeros
function padWithZero(num) {
    return num.toString().padStart(2, '0');
}

// Function to update the countdown
function updateCountdown() {
    // const countdownBox = document.getElementById('countdown-box');
    const eventBox = document.getElementById('event-box'), dayBox = document.getElementById('day'),
        hourBox = document.getElementById('hour'), minBox = document.getElementById('min'),
        secBox = document.getElementById('sec'), evenDate = Date.parse(eventBox.textContent);


    setInterval(() => {
        const now = new Date().getTime();
        const diff = evenDate - now;

        if (diff >= 0) {
            const d = Math.floor(diff / (1000 * 60 * 60 * 24));
            const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const m = Math.floor((diff / (1000 * 60)) % 60);
            const s = Math.floor((diff / 1000) % 60);

            // countdownBox.innerHTML = `${padWithZero(d)} : ${padWithZero(h)} : ${padWithZero(m)} : ${padWithZero(s)}`;
            dayBox.innerHTML = padWithZero(d);
            hourBox.innerHTML = padWithZero(h);
            minBox.innerHTML = padWithZero(m);
            secBox.innerHTML = padWithZero(s);

            // console.log(countdownBox.innerHTML);
        }

    }, 1000);
}

// Call the function to start the countdown
updateCountdown();




