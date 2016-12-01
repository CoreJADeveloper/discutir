jQuery(document).ready(function($){

	tinymce.init({
		selector: '#answer_textarea'
	});

	$('#answer-question-modal').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget) 
		var question_id = button.attr('id')
		var modal = $(this);
		modal.find('.hidden-question-id').val(question_id)
	});

	$('#ask-question-modal').on('show.bs.modal', function (event) {
		var pathname = window.location.pathname; 
		// var url      = window.location.href;     
		var button = $(event.relatedTarget) 
		var recipient = button.data('whatever') 
		var modal = $(this)
		modal.find('.modal-title').text('Ask a question')
		$.ajax({
			url : "/ask-question/", 
			type : "POST", 
			data : {
				"request_type": "ask_question"
			}, 
			beforeSend: function(xhr, settings) {
				function getCookie(name) {
	             	var cookieValue = null;
	             	if (document.cookie && document.cookie != '') {
		                var cookies = document.cookie.split(';');
		                for (var i = 0; i < cookies.length; i++) {
			                var cookie = jQuery.trim(cookies[i]);
			                if (cookie.substring(0, name.length + 1) == (name + '=')) {
			                	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			                	break;
			                }
		                }
            		}
            		return cookieValue;
	        	}
		        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
		        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		        }
	        }, 
			success : function(data_object) {	
				var $response = $(data_object);  
				$response.filter('.chosen-select-question').chosen({no_results_text: "Oops, nothing found!", width: "100%"}); ; 
        		$response.find('.chosen-select-question').chosen({no_results_text: "Oops, nothing found!", width: "100%"}); ; 
				modal.find('.modal-body').html($response)
				// $(".chosen-select-question").chosen({no_results_text: "Oops, nothing found!"}); 
	        },
	        error : function(xhr,errmsg,err) {
	        	console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	})

	$('.poll-form').on('submit', function(event){
		event.preventDefault();
		$('#loading-ajax').removeClass('hide')
	    console.log("form submitted!");  // sanity check
	    var form_id = $(this).attr('id');
	    insert_vote(form_id);
	});

	$('#ask-question-form').on('submit', function(event){
		event.preventDefault();
		$('#loading-ajax').removeClass('hide')
	    var form = $(this);
	    submit_question(form);
	});

	$('#answer-question-form').on('submit', function(event){
		event.preventDefault();
		$('#loading-ajax').removeClass('hide')
	    var form = $(this);
	    answer_question(form);
	});

	$(".chosen-select").chosen({no_results_text: "Oops, nothing found!"}); 

	function answer_question(form){
		$.ajax({
			url : "/answer-question", 
			type : "POST", 
			data : $(form).serialize(), 

			success : function(data_object) {
	        	$('#loading-ajax').addClass('hide')
	        	$('#answer-question-modal').modal('toggle');
	        	 location.reload(); 
	        },

	        error : function(xhr,errmsg,err) {
	        	console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	}

	function submit_question(form){
		$.ajax({
			url : "/submit-question", 
			type : "POST", 
			data : $(form).serialize(), 

			success : function(data_object) {
	        	$('#loading-ajax').addClass('hide')
	        	$('#ask-question-modal').modal('toggle');
	        },

	        error : function(xhr,errmsg,err) {
	        	console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	}

	function insert_vote(form_id){
		var form_id = form_id;
		$.ajax({
			url : "/", 
			type : "POST", 
			data : $('#'+form_id).serialize(), 

			success : function(data_object) {
	        	// console.log(data_object)
	        	$('#loading-ajax').addClass('hide')
	        	if (data_object == 'Success') {
	        		$('#success-message').removeClass('hide');
	        	}
	        	else if (data_object == 'Exists') {
	        		$('#danger-message').removeClass('hide');
	        	}
	        	else if (data_object == 'User not authenticated') {
	        		$('#warning-message').removeClass('hide');
	        	}
	        	else if (data_object == 'Select option') {
	        		$('#select-choice-message').removeClass('hide');
	        	}
	        },

	        error : function(xhr,errmsg,err) {
	        	console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	}
})

