
$('#favorite-form').on('submit', function(event){
    event.preventDefault();
    var csrf = $('[name=csrfmiddlewaretoken]');
    var id = document.getElementById("id").value;
    $.ajax({
        type: "POST",
        url: '/product/'+id+'/favorite/',
        data: {
            'csrfmiddlewaretoken': csrf.attr('value')
        }
    });
});
