console.log("working fine");

const monthNames = ["Jan", "Feb", "Mar", "April", "May",
                   "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec",
];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved to DB");

            if(res.bool == true){
                $("#review-res").html("Review added successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html =  '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="thumb text-center">'
                    _html +='<img src="https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg" alt="" />'
                    _html +='<a href="#" class="font-heading text-brand">' + res.context.user + '</a>'
                    _html +='</div>'

                    _html +='<div class="desc">'
                    _html +='<div class="d-flex justify-content-between mb-10">'
                    _html +='<div class="d-flex align-items-center">'
                    _html +='<span class="font-xs text-muted">' + time + '</span>'
                    _html +='</div>'

                    for(let i = 1; i<=res.context.rating; i++ ){
                        _html += '<i class=" fas fa-star text-warning"></i>'
                    }
                    
                    _html +='</div>'
                    _html +='<p class="mb-10">'+ res.context.review +' </p>'

                    _html +='</div>'
                    _html +='</div>'
                    _html +='</div>'
                    $(".comment-list").prepend(_html)


            }


        }
        })
})  


$(".add-to-cart-btn").on("click", function(){

    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).val()

    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price -" + index).text()

    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("ID:", product_id);
    console.log("PID:", product_pid); 
    console.log("Image:", product_image); 
    console.log("Index:", index); 
    console.log("Current Element:", this_val);


    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding Product To Cart...");
        },
        success: function(response){
            this_val.html("Product added to cart")
            console.log("Added Product To Cart!");
            $(".cart-items-count").text(response.totalcartitems)

        }
    })
})



// Добавлять в корзину
// $(".add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)


//     console.log("Quantity:", quantity);
//     console.log("Title:", product_title);
//     console.log("Price:", product_price);
//     console.log("ID:", product_id);
//     console.log("Current Element:", this_val);


//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding Product To Cart...");
//         },
//         success: function(response){
//             this_val.html("Product added to cart")
//             console.log("Added Product To Cart!");
//             $(".cart-items-count").text(response.totalcartitems)

//         }
//     })
// })