
$('#favorite-form').on('submit', function(event){
    event.preventDefault();
    var csrf = $('[name=csrfmiddlewaretoken]');
    var product_id = document.getElementById("id").value;
    $.ajax({
        type: "POST",
        url: `/product/${product_id}/favorite/`,
        data: {
            'csrfmiddlewaretoken': csrf.attr('value')
        },
        success: function(data, status, xhr) {
            if (data) {
                window.location.replace(data['url']);
            } else if (xhr.status == 200) {
                $('#favorite-form .button-favorite').css('color', '#999');
            } else if (xhr.status == 201) {
                $('#favorite-form .button-favorite').css('color', 'red');
            }
        },
        error: function(data) {
            console.log(data);
        }
    })
});
