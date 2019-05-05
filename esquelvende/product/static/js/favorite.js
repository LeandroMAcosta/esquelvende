
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
            if (xhr.status == 205) {
                console.log("Lo borro");
            } else if (xhr.status == 201) {
                console.log("Lo creo");
            }
        },
        error: function() {
            console.log("Todo mal");
        }
    })
});
