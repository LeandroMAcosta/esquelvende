function republishProduct(){
    var obj = event.target,
        id_product = obj.value,
        csrf = obj.parentElement.firstElementChild.value;

    $.ajax({
        url: `/product/${id_product}/republish/`,
        type: "POST",
        data: {
            'csrfmiddlewaretoken': csrf
        }
    })
    .done(function(data) {
        $('.product-list p-2').html(data);
    })
    .fail(function(xhr) {
        alert("Error en el server. Intente de nuevo.")
    }); 

}
