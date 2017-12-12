$(function(){
	$('#btnRegister').click(function(){

		$.ajax({
			url: '/saveUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
