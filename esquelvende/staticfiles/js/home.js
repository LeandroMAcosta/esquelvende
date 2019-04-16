// Para que en el cel se pueda scrollear en los productos
$('.container').ready(function() {
    if (isMobile.mobilecheck()) { 
        $('.scroll-photos').css("overflow-x", "auto");
    }
});

$(".prev-button").click(function() {
    var photos = $(this).next(); 
    $(photos).animate({
        scrollLeft: '-=400'
    }, 500, 'swing');
});

$(".next-button").click(function() {
    var photos = $(this).prev(); 
    $(photos).animate({
        scrollLeft: '+=400'
    }, 500, 'swing');
});

$(".carousel-container").mouseover(function() {
    var parent = $(this).children()[1],
        countChild = $(parent).children().length,
        containerWidth = $('.container').width(),
        boxWidth = $('.redirect-product').width();

  /* 
  El + 30 es por el margin que tiene el container, este if
  es para que no muestre las fechas sin tener demasiados productos
  */
    if ((countChild * boxWidth + 30) > containerWidth) {
        var children = $(this).children(),
            prev = children[0],
            next = children[2],
            childPrev = prev.children[0],
            childNext = next.children[0];
        if (!isMobile.mobilecheck()) {
            next.classList.remove("disabled");
            prev.classList.remove("disabled");
            childPrev.classList.remove("disabled");
            childNext.classList.remove("disabled");
        }
    }
});

$(".carousel-container").mouseout(function() {
    var children = $(this).children(),
        prev = children[0],
        next = children[2],
        childPrev = next.children[0],
        childNext = next.children[0];
    if (!isMobile.mobilecheck()) {
        next.classList.add("disabled");
        prev.classList.add("disabled");
        childPrev.classList.add("disabled");
        childNext.classList.add("disabled");
    }
});

if (!isMobile.mobilecheck()) {
    $(".item").mouseover(function() {
        var children = $(this).children(),
            whatsappLink = children[0],
            whatsappIcon = $(children[0]).children()[0];
        
        if (whatsappLink && whatsappIcon) {
            whatsappLink.classList.remove("disabled");
            whatsappIcon.classList.remove("disabled");
        }
    });

    $(".item").mouseout(function() {
        var children = $(this).children(),
            whatsappLink = children[0],
            whatsappIcon = $(children[0]).children()[0];

        if (whatsappLink && whatsappIcon) {
            whatsappLink.classList.add("disabled");
            whatsappIcon.classList.add("disabled");
        }
    });
} else {
    $('a.whatsapp-link').removeClass("disabled");
    $('i.whatsapp').removeClass("disabled");
}