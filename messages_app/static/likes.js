// likes.js

$(document).ready(function() {
    $('.like-button').on('click', function(event) {
        event.preventDefault();
        var pk = $(this).attr('data-post-id');
        var url = '/postList/'+str(pk)+'/like/';
        $.ajax({
            url: url,
            method: 'POST',
            data: {'pk': pk},
            success: function(response) {
                var likes = response.likes;
                $('#likes-count-' + post_id).text(likes);
            }
        });
    });
});
