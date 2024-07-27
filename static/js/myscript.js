// Handle quantity increment
$(".plus-cart").click(function() {
    var id = $(this).attr("pid").toString();
    var eml = $(this).siblings("span"); 
    $.ajax({
        type: "GET",
        url: "/plus_Cart",
        data: { prod_id: id },
        success: function(data) {
            eml.text(data.quantity); // Update quantity
            $("#amount").text("Kshs. " + data.amount); // Update amount
            $("#total_amount").text("Kshs. " + data.totalamount); // Update total amount
        }
    });
});

// Handle quantity decrement
$(".minus-cart").click(function() {
    var id = $(this).attr("pid").toString();
    var eml = $(this).siblings("span"); 
    $.ajax({
        type: "GET",
        url: "/minus_Cart",
        data: { prod_id: id },
        success: function(data) {
            eml.text(data.quantity); // Update quantity
            $("#amount").text("Kshs. " + data.amount); // Update amount
            $("#total_amount").text("Kshs. " + data.totalamount); // Update total amount
        }
    });
});

// Handle remove item
$(".remove-cart").click(function(e) {
    e.preventDefault(); // Prevent default action
    var id = $(this).attr("pid").toString();
    var row = $(this).closest('.row'); // Find the closest row to remove
    $.ajax({
        type: "GET",
        url: "/remove_Cart",
        data: { prod_id: id },
        success: function(data) {
            row.remove(); // Remove item from the cart
            $("#amount").text("Kshs. " + data.amount); // Update amount
            $("#total_amount").text("Kshs. " + data.totalamount); // Update total amount
        }
    });
});

// Handle adding to wishlist
$('.plus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: { prod_id: id },
        success: function() {
            window.location.href = `/product-details/${id}`;
        }
    });
});

// Handle removing from wishlist
$('.minus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: { prod_id: id },
        success: function() {
            window.location.href = `/product-details/${id}`;
        }
    });
});
