let type_data = {
    variant: 0,
    image: 0,
};

function calculate(duration, percent, price, status, id) {
    if (status === "images") {
        type_data.image = {
            id: id,
            price: price
        }
        if (type_data.variant === 0) {
            var image_total = price + ((percent * price) / 100);
            var image_monthly = image_total / duration;

        } else {
            var image_total = price + ((type_data.variant.percent * price) / 100);
            var image_monthly = image_total / type_data.variant.duration;
        }
        image_monthly = image_monthly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
        image_monthly = image_monthly + " uzs/oy";
        price = price + " uzs";
        $("#monthly").text(image_monthly);
        $("#origin_price").text(price);
    } else {
        type_data.variant = {
            id: id,
            duration: duration,
            percent: percent
        }
        if (type_data.image === 0) {
            var total = price + ((percent * price) / 100);
            var monthly = total / duration;
        } else {
            var total = type_data.image.price + ((percent * type_data.image.price) / 100);
            var monthly = total / duration;
            price = type_data.image.price + " uzs";
        }
        monthly = monthly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
        monthly = monthly + " uzs/oy";

        $("#monthly").text(monthly);
        $("#origin_price").text(price);
    }
}

// ================================================ Banner Deadline ====================================================

const eventBox = document.getElementById('event-box');
const dayBox = document.getElementById('day');
const hourBox = document.getElementById('hour');
const minBox = document.getElementById('min');
const secBox = document.getElementById('sec');
// console.log(eventBox.textContent);

const evenDate = Date.parse(eventBox.textContent);
// console.log(evenDate);

setInterval(() => {
    const now = new Date().getTime();
    // console.log(now);

    const diff = evenDate - now;
    // console.log(diff);

    const d = Math.floor(evenDate / (1000 * 60 * 60 * 24 ) - (now / (1000 * 60 * 60 * 24)));
    const h = Math.floor((evenDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24);
    const m = Math.floor((evenDate / (1000 * 60) - (now / (1000 * 60))) % 60);
    const s = Math.floor((evenDate / (1000) - (now / (1000))) % 60);
    // console.log(m);
    // console.log(s);

    if (diff >= 0) {
        // countdownBox.innerHTML = `${d.toString().padStart(2, '0')} : ${h.toString().padStart(2, '0')} : ${m.toString().padStart(2, '0')} : ${s.toString().padStart(2, '0')}`;
        dayBox.innerHTML = `${d.toString().padStart(2, '0')}`;
        hourBox.innerHTML = `${h.toString().padStart(2, '0')}`;
        minBox.innerHTML = `${m.toString().padStart(2, '0')}`;
        secBox.innerHTML = `${s.toString().padStart(2, '0')}`;
        // console.log(countdownBox.innerHTML);
    }

}, 1000);



