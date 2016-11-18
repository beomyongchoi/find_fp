$("#comment").focus(function() {
    $("#sign-in-please").fadeIn();
});

$("#comment").blur(function() {
    $("#sign-in-please").fadeOut();
});

$("#comment-form").submit(function(e) {
    $.ajax({
        url: '/videos/comment/',
        data: $("#comment-form").serialize(),
        cache: false,
        type: 'post',
        success: function(data) {
            $("#comment-list").html(data);
            var comment_count = $("#comment-list .comment").length;
            $(".comment-count").text(comment_count);
            $("#comment").val("");
            $("#comment").blur();
        }
    });
    e.preventDefault();
});

$("#disabled").prop('disabled', true);

document.addEventListener( "DOMContentLoaded", function() {
    var popcorn = Popcorn("#video");

    popcorn.play();
});
