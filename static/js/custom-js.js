$('#password1, #password2').on('keyup', function () {
  if ($('#id_password1').val() == $('#id_password2').val()) {
    $('#message').html('Matching').css('color', 'green');
  } else 
    $('#message').html('Not Matching').css('color', 'red');
});