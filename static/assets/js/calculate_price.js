function calculate(duration, percent, price) {
    var total = price + ((percent * price) / 100);
    var monthly = total / duration;
    monthly = new Intl.NumberFormat('de-DE').format(monthly);
    total = new Intl.NumberFormat('de-DE').format(total);
    total = total + " UZS";
    monthly = monthly + " UZS";
    $("#div_main").show();
    $("#total").text(total);
    $("#monthly").text(monthly);
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



