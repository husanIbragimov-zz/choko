var size = 0
$(".size_class li").on("click", function () {
    size = $(this).text();

});

$('.addToCartBtn').on('click', function () {
    var product_id = $('.prod_id').val()
    var quantity = $('.qty-input').val()
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        method: 'POST',
        url: "/order/add-to-cart/",
        data: {
            "product_id": product_id,
            "quantity": quantity,
            "size": size,
            csrfmiddlewaretoken: token
        },
        success: function (response) {
            console.log(response.status)
            if (response.status) {
                alertify.success(response.msg)

            } else {
                alertify.error(response.msg)
            }
        }
    })

})

