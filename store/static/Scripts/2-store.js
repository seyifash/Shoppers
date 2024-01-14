document.addEventListener('DOMContentLoaded', function () {
    let picsDescriptions = document.querySelectorAll('.pics-description');
    picsDescriptions.forEach(function(picsDescription) {
        picsDescription.addEventListener('click', function() {
            const productId = this.getAttribute('id');
            console.log(productId);
            window.location.href = `/selected_item/${productId}`;
        });
    });
});