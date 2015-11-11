var outer;
$(function() {
    $(".showmenu").click(function() {
        $(this).parent().hide();
        $(this).parents('.date-bar').next().show();
    });
});