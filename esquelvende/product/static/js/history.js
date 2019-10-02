$(document).ready(function(){
    var csrf = $('[name=csrfmiddlewaretoken]');
    var product_id = document.getElementById("id").value;
    $.ajax({
        url: `/product/${product_id}/history/`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf.attr('value')
        },
        success: function(data, status, xhr){
            console.log(data)
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.responseText)
        }
    });
});