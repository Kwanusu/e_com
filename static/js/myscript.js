

$(".plus_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2] 
    $.ajax({
        type: "GET",
        url: "/plus_Cart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$(".minus_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2] 
    $.ajax({
        type: "GET",
        url: "/minus_Cart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})


$(".remove_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this 
    $.ajax({
        type: "GET",
        url: "/remove_Cart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            eml = parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type : "GET",
        url : "/pluswishlist",
        data: {
            prod_id:id
        },
        success:function(){
            window.location.href = `http://localhost:8000/product-details/${id}`
        }
    })
})

$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type : "GET",
        url : "/minuswishlist",
        data: {
            prod_id:id
        },
        success:function(){
            window.location.href = `http://localhost:8000/product-details/${id}`
        }
    })
})