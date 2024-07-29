

$(".plus_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2] 
    $.ajax({
        type: "GET",
        url: "/plus_Cart",
        data: { prod_id: id },
        success: function(data){
            if (data.error) {
                alert(data.error);
            } else {
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        }
    });
});

$(".minus_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2] 
    $.ajax({
        type: "GET",
        url: "/minus_Cart",
        data: { prod_id: id },
        success: function(data){
            if (data.error) {
                alert(data.error);
            } else {
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        }
    });
});

$(".remove_cart").click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/remove_Cart",
        data: { prod_id: id },
        success: function(data){
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                eml.parentNode.parentNode.parentNode.parentNode.remove();
            }
        }
    });
});

$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: { prod_id: id },
        success: function(){
            window.location.href = `http://localhost:8000/product-details/${id}`;
        }
    });
});

$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: { prod_id: id },
        success: function(){
            window.location.href = `http://localhost:8000/product-details/${id}`;
        }
    });
});

{/* <script>
document.addEventListener('DOMContentLoaded', () => {
    // Remove item from cart
    const removeCartItemButtons = document.querySelectorAll('.remove-cart');
    removeCartItemButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            const productId = event.target.getAttribute('pid');
            
            try {
                const response = await fetch('{% url "remove_Cart" %}', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({ prod_id: productId })
                });

                if (response.ok) {
                    const cartItem = document.getElementById('cart-item-' + productId);
                    cartItem.remove();
                    alert('Item removed from cart!');
                    updateCartDetails(); // Update cart details after removal
                } else {
                    throw new Error('Failed to remove item from cart.');
                }
            } catch (error) {
                console.error('Error removing item from cart:', error);
            }
        });
    });

    // Update quantity in cart
    const updateCartQuantity = async (productId, quantity) => {
        try {
            const response = await fetch('{% url "update_cart_quantity" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({ prod_id: productId, quantity: quantity })
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('quantity-' + data.cart_item_id).textContent = data.quantity;
                updateCartDetails(); // Update cart details after quantity change
            } else {
                throw new Error('Failed to update quantity in cart.');
            }
        } catch (error) {
            console.error('Error updating quantity in cart:', error);
        }
    };

    // Event listeners for plus and minus cart buttons
    const minusCartItemButtons = document.querySelectorAll('.minus-cart');
    minusCartItemButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const productId = event.target.getAttribute('pid');
            const quantityElement = document.getElementById('quantity-' + productId);
            let quantity = parseInt(quantityElement.textContent);

            if (quantity > 1) {
                quantity--;
                updateCartQuantity(productId, quantity);
            }
        });
    });

    const plusCartItemButtons = document.querySelectorAll('.plus-cart');
    plusCartItemButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const productId = event.target.getAttribute('pid');
            const quantityElement = document.getElementById('quantity-' + productId);
            let quantity = parseInt(quantityElement.textContent);

            quantity++;
            updateCartQuantity(productId, quantity);
        });
    });

    

    // Function to update cart details
    const updateCartDetails = async () => {
        try {
            const response = await fetch('{% url "show_cart" %}');
            if (response.ok) {
                const data = await response.json();
                document.getElementById('amount').textContent = 'Kshs. ' + data.total_amount;
                document.getElementById('total-amount').textContent = 'Kshs. ' + data.total_amount;
            } else {
                throw new Error('Failed to fetch cart details.');
            }
        } catch (error) {
            console.error('Error updating cart details:', error);
        }
    };
}); */}
