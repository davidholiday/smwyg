// makes it so alert messages dismiss themselves
// copyright (c) 2018 wildduck.io

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);