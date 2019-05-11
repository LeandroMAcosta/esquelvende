function changeStatus() {
    var obj = event.target,
        parent = $(obj.parentElement).next()[0];
    if ($(parent).hasClass('hidden')) {
        parent.classList.remove("hidden");
        $(obj).html("Ocultar")
    } else {
        parent.classList.add("hidden");
        $(obj).html("Mostrar")
    }
}