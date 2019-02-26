const images = document.querySelector("div#images");
const urlCreator = window.URL || window.webkitURL;
var obj = {};
let size = 0;

function uploadFile(files) {
    for(let i = 0; i < files.length && Object.keys(obj).length < 6; ++i) {
        obj[i + size++] = files.item(i);
    }
    renderFiles();
}

function deleteFile(div, key) {
    changeNumberImages(1)
    delete obj[key];
    images.removeChild(images.querySelector(`div#images div.id${key}`));
}

function renderFiles() {
    for (let [key, file] of Object.entries(obj)) {
        
        // If it already exists move to the next file.
        if(document.querySelector(`div#images img.id${key}`)) continue;

        // If it doesnt exists we create it.
        var parent = document.createElement("div"),
            newImage = document.createElement("img"),
            deleteImage = document.createElement("img");

        deleteImage.setAttribute("src", "../static/remove.svg");
        deleteImage.setAttribute("title", "Eliminar foto");

        parent.classList.add(`id${key}`, "d-flex", "justify-content-end");
        newImage.classList.add(`id${key}`, "file-loader");
        deleteImage.classList.add(`deleteImg`, `id${key}`);

        deleteImage.onclick = () => { deleteFile(newImage, key) };

        const imageUrl = urlCreator.createObjectURL(file);
        newImage.src = imageUrl;

        parent.appendChild(newImage);
        parent.appendChild(deleteImage);
        images.appendChild(parent);

        // clean entry. 
        document.getElementsByClassName("form-control-file")[0].value = "";

        changeNumberImages(0)
    }
}

$('#check').keyup( function() {
    var value = $(this).val(),
        maxlength = $(this).data("maxlength"),
        count = maxlength - value.length;
    if (count >= 0) {$("#counter").html(`Restan ${count} caracteres.`)}
});

// Si es un celular cambia el height de la caja de categorias.
$('.div-category').ready(function() {
    if (isMobile.mobilecheck()) $('.div-category').css("height", "auto");
});

function categorySelector(event) {
    var current = event.target,
        parent = current.closest('.container-categories');

    next_category = {'category': 'sub_a', 'sub_a':'sub_b', 'sub_b': 'brand'}

    $.get('/load-categories/', { category: current.id, id_category: current.value, next_category: next_category[current.name] }, function(data) {
        let id = data['id'];
        delete data['id'];

        // Si tiene hermanos los borramos.
        while(document.getElementById(`d-${current.id}`).nextElementSibling) {
            parent.removeChild(document.getElementById(`d-${current.id}`).nextElementSibling);
        }
        
        if (Object.keys(data).length != 0) {
            let newCategory = document.createElement("div");
            let newSelect = document.createElement("select");

            newCategory.setAttribute("id", `d-id_${id}`);
            newCategory.classList.add("div-category");

            const attr = {id: `id_${id}`, name: id, size: 11};
            
            /* IsMobile en este caso lo utilizo para cambiar el tamaño del 
               div que contiene las categorias en caso que sea un celular. */
            if (isMobile.mobilecheck()) {
                newCategory.style.height = 'auto';
            }

            for (let [key, value] of Object.entries(attr)) {
                newSelect.setAttribute(key, value);
            }

            newSelect.classList.add("select-category");
            newSelect.setAttribute("required", "");
            newSelect.addEventListener("change", categorySelector);

            parent.appendChild(newCategory);
            newCategory.appendChild(newSelect);    

            $.each(data, function(idx, category){                          
               $(`#id_${id}`).append(`<option value=${idx}>${category}</option>`);
            });
        }
    });
}


function displacement() {

    /* En realidad no habrìa que fijarlo en 1000, si no,
       ver bien cuanto ocupa cada imagen. */
    $(".scroll-photos").scrollLeft(1000);
}

function changeNumberImages(isDelete) {
    var countImages = $('#images').children().length;
    if (isDelete) {
        console.log(countImages, 6 - countImages)
        countImages = 6 - countImages + 1;
    } else {
        countImages = 6 - countImages;
    }
    $("#photos").html(`+${countImages} fotos`);
}

function sendPhotos(e) {
    // Cancela el POST del formulario para usar solo AJAX.
    e.preventDefault();
    var fd = new FormData();

    // Para hacer un POST django nos pide el csrf.
    var $csrf = $('[name=csrfmiddlewaretoken]');

    var fields = {
        'title': $('[name=title]').val(),
        'category': $('[name=category]').val(),
        'sub_a': $('[name=sub_a]').val(),
        'sub_b': $('[name=sub_b]').val(),
        'brand': $('[name=brand]').val(),
        'status': $('[name=status]').val(),
        'contact_phone': $('[name=contact_phone]').val(),
        'whatsapp': $('[name=whatsapp]').val(),
        'contact_email': $('[name=contact_email]').val(),
        'description': $('[name=description]').val(),
        'price': $('[name=price]').val()
    }
    console.log(fields)
    for (let [key, value] of Object.entries(fields)) {
        if (value) fd.append(key, value);
    }

    for (let [key, file] of Object.entries(obj)) {
        fd.append('image', file);
    }

    fd.append('csrfmiddlewaretoken', $csrf.attr('value'))

    $.ajax({
        url: "/publish/",
        type: 'POST',
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',

        success: function(data, status, xhr) {
            if (data.err_code) {
                for(var key in data.err_msg) {
                    let newDiv = document.createElement("div");
                    let newMsg = document.createTextNode(`${data.err_msg[key][0]}`)

                    elem = document.querySelector(`[for=${key}]`);
                    parent = elem.parentElement;
                    
                    // Si ya existe un error lo borramos y ponemos el nuevo.
                    if (parent.querySelector("div.alert")) {
                        parent.removeChild(parent.querySelector("div.alert"));
                    }

                    newDiv.classList.add("alert", "alert-danger");

                    // Colocamos el error en el html.
                    parent.insertBefore(newDiv, elem);
                    newDiv.appendChild(newMsg);
                }
            } else {
                /* Usar replace permite que la pagina actual no se
                   guarde en el historial de sesion, lo que significa
                   que no vamos a poder volver por el boton para atras. */
                window.location.replace(`/product/${data.id_product}/`);
            }
            
        },
        error: function(xhr, status, error) {
            alert("Algo salio mal, vuelva a recargar la pagina.");
        }
    });

}