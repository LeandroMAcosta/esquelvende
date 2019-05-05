
$('#favorite-form').on('submit', function(event){
    event.preventDefault();
    var csrf = $('[name=csrfmiddlewaretoken]');
    var id = document.getElementById("id").value;
    $.ajax({
        type: "POST",
        url: '/product/'+id+'/favorite/',
        data: {
            'csrfmiddlewaretoken': csrf.attr('value')
        },
        success: function(data, status, xhr) {
            console.log(xhr);
            if (xhr.status == 204) {
                $('#favorite-form .button-favorite').css('color', '#999');
                console.log("Lo borro");
            } else if (xhr.status == 201) {
                $('#favorite-form .button-favorite').css('color', 'red');
                console.log("Lo creo");
            } else {
                // print(data['url'])
                window.location.replace(data['url']);
            }
        },
        error: function(data) {
            console.log(data);
        }
    })
});
