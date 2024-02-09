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

console.log(isAuthenticated);
if (isAuthenticated == 'True') {
    let anchor = document.querySelector('#login-box a');
    console.log(anchor.innerText);
    anchor.href = '/logout';
    anchor.innerText = 'Logout';
    console.log(anchor.href);
} else {
    let anchor = document.querySelector('#login-box a');
    console.log(anchor.innerText);
    anchor.href = '/login';
    anchor.innerText = 'Login';
    console.log(anchor.href);
    console.log('User is not authenticated.');
}


