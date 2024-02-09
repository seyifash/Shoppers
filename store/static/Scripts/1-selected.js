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
            if(!isAuthenticated){
                console.log('Not logged in')
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
        if (!isAuthenticated) {
            console.log('Not logged in');
        } else {
            updateCartItem(productSize, productColor, productId, action);
            console.log('user is logged in, sending data');
        }
    });
});



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