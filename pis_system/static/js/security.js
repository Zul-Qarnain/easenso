/*function searchRegStud(form){
  var search_text = $('#'+ form + " #search-text").val();
  //search option
  
  var search_opt = $('#name-search').val();
  //request processor
  var server = '/registration/searchRegStud'
    
  if(search_opt=='section'){
      search_text = $("#section-list").val();
  }
  //sending request 
  $.get(server, {search: search_text, option:search_opt}, function(data){
      //receive and render response
	$('#stud_list').html(data);
  });
}

function set_edit_emp(username){
    $.get('/registration/new_employee', {'username':username}, function(emp_form){
	$("#emp_form").html(emp_form);
    });
}
*/

//global variables
var valid_employee = true;



//function definitions

function viewEmpProfile(username){
    request = {username: username};
    $.get('/security/employee_profile', request, 
	  function(data){
	      $("#profile").html(data);
	  });
}

function validateEmployee(){
    request = {firstname: $('#id_firstname').val(),
               lastname: $('#id_lastname').val()};
    alert(request.firstname +' '+ request.lastname);
    $.get('/security/is_employee_name_exist', request, function(response){
	response = new String(response).trim();
	alert(response);
	if(response == 'has_duplicate'){
	    valid_employee = false;
	}else{
	    valid_employee = true;
	}
    });
    return valid_employee;
}

$('#gen_emp_id_btn').click(function(){
    $.ajax({
	url : '/security/generate_employee_id',
	dataType : 'html',
	success : function(data){
	    $("#id_username").val(data);
	}
    });
});

$("#id_username").keydown(function(e){
    return allNumbers(e);
});


