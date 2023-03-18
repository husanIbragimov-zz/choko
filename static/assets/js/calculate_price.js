let type_data = {
    variant: 0,
    image: 0,
}

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
