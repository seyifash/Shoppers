$(document).ready(function () {
    let dangerBtnClicked = false;

    // Click event for the danger-btn
    $('.danger-btn').click(function () {
      $('.the-alert-danger').hide();
      dangerBtnClicked = true;
    });

    // Set timeout to hide the alert-danger if danger-btn is not clicked
    setTimeout(function () {
      if (!dangerBtnClicked) {
        $('.the-alert-danger').hide();
      }
    }, 3000);

    // Click event for the close-btn
    let successBtnClicked = false;
    $('.close-btn').click(function () {
      $('.the-alert-success').hide();
      successBtnClicked = True;
    });

    setTimeout(function () {
        if (!successBtnClicked) {
          $('.the-alert-danger').hide();
        }
      }, 5000);
  });