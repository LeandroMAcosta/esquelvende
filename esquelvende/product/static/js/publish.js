
var isMobile = {
    mobilecheck : function() {
        return (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino|android|ipad|playbook|silk/i.test(navigator.userAgent||navigator.vendor||window.opera)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test((navigator.userAgent||navigator.vendor||window.opera).substr(0,4)))
    }
}

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
        let parent = document.createElement("div");
        let newImage = document.createElement("img");
        let deleteImage = document.createElement("img");

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
    let value = $(this).val();
    let maxlength = $(this).data("maxlength");
    let count = maxlength - value.length;
    if (count >= 0) {$("#counter").html(`Restan ${count} caracteres.`)}
});

// Si es un celular cambia el height de la caja de categorias.
$('.div-category').ready(function() {
    if (isMobile.mobilecheck()) $('.div-category').css("height", "auto");
});

function categorySelector(event) {
    let current = event.target; 
    let parent = current.closest('.container-categories');

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
    console.log(countImages)
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