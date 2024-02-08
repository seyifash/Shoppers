document.addEventListener('DOMContentLoaded', function () {
    let products = document.querySelectorAll('.cart');
    products.forEach(function(product) {
        product.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            console.log(productId);
            window.location.href = `/selected_item/${productId}`;
        });
    });
});
document.getElementById("continue-to").addEventListener("click", function() {
    window.location.href = "/store";
});

var navbarItems = document.querySelectorAll('ul.navbar li');

// Loop through each list item
navbarItems.forEach(function(item) {
    // Check if the inner text of the list item is "Login"
    if (item.innerText.trim() === "Login") {
        // Log the inner text of the found list item
        console.log(item.innerText);
    }
});

   /* signIn.addEventListener('click', () => {
        if (is_authenticated){
            console.log(signIn.innerText);
        }
});*/