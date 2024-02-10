let productSize;
let productColor;

const colors = document.querySelectorAll('.col2');
    colors.forEach((color) => {
        color.addEventListener('click', () => {
            productColor = color.textContent.trim().replace('•', '');
            console.log(productColor);
    });
});

const sizes = document.querySelectorAll('.size-button');
    sizes.forEach((size) => {
        size.addEventListener('click', () => {
            productSize = size.textContent.trim();
            console.log(productSize);
        });
    });

const addBtn = document.querySelector('.update-cart');
if(addBtn){
    addBtn.addEventListener('click', () => {
        if (productSize && productColor) {
            const productId = addBtn.dataset.product;
            const action = addBtn.dataset.action;
            if(isAuthenticated == 'False'){
                addToCookieItem(productId, action, productColor, productSize);
            }else {
                updateCartItem(productSize, productColor, productId, action);
                console.log('user is logged in, sending data');
            }
        } else {
            console.log('select a size and color');
        }
});
} else {
    console.log("Element with class 'update-cart' not found.");
}

const addBtnCart = document.querySelectorAll('.update-Cart-btn');
addBtnCart.forEach((btn) => {
    btn.addEventListener('click', () => {
        const productId = btn.dataset.product;
        const action = btn.dataset.action;
        console.log(productId);
        console.log(action);
        if (isAuthenticated == 'False') {
            addToCookieItem(productId, action, productColor, productSize);
        } else {
            updateCartItem(productSize, productColor, productId, action);
            console.log('user is logged in, sending data');
        }
    });
});
function addToCookieItem(productId, action, productColor, productSize){
    console.log('This user is not authenticated');
    if(action == 'add') {
        if(cart[productId] == undefined) {
            cart[productId] = {
                'quantity': 1,
                'productColor': productColor,
                'productSize': productSize
            };
        }else{
            cart[productId]['quantity'] += 1
            if(cart[productId]['productColor'] != productColor || cart[productId]['productSize'] != productSize){
                    cart[productId]['productColor'] = productColor
                    cart[productId]['productSize'] = productSize
            }
        }
    }
    if(action == 'remove') {
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity']  <= 0){
            console.log('Remove Item');
            delete cart[productId]
        }
    }
    console.log('cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain;path=/"
    location.reload()


}


function updateCartItem(productSize, productColor, productId, action) {
    let url = '/updateItem'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'productSize': productSize, 'productColor': productColor, 'productId': productId, 'action': action})
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}