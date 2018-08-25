function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      console.log("La concha de la lora");  
      $('.avatar-container .avatar').css({'backgroundImage': `url(${e.target.result})`});
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$(".avatar-container #id_avatar").change(function () {
  readURL(this);
});