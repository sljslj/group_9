(function ($) {
    $.fn.extend({
        collect: function () {
            $.ajax({
                type: 'POST',
                data: {
                filmname: $(this).name,
                },
                success: function (result) {
                    $(this).text(result.message)
                },
                error: function (result) {
                    alert(result.message)
                },
            })
        }
    })
})(JQuery);