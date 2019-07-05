function deleteProduct(){
    event.preventDefault();
    var obj = event.target,
        id_product = obj.value,
        csrf = obj.parentElement.firstElementChild.value;
    $.ajax({
        url: `/product/${id_product}/delete/`,
        type: "POST",
        data: {
            'csrfmiddlewaretoken': csrf
        }
    })
    .done(function(data) {
        var node = data['id_product'];
        document.getElementById(node).remove();
    })
    .fail(function(xhr) {
        alert("Error en el server. Intente de nuevo.")
    });
}