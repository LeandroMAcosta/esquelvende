function deleteProduct(){
    event.preventDefault();
    var obj = event.target,
        product_id = obj.value,
        csrf = obj.parentElement.firstElementChild.value;
    $.ajax({
        url: `/product/${product_id}/delete/`,
        type: "POST",
        data: { 'csrfmiddlewaretoken': csrf }
    })
    .done(function(data) {
        var node = data['product_id'];
        document.getElementById(node).remove();
    })
    .fail(function(xhr) {
        alert("Error en el server. Intente de nuevo.")
    });
}