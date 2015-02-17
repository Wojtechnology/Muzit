// JavaScript :: Controller
// Author: Wojtek Swiderski
// Main data controller for the website

// SECTION - JQuery Functions

// Toggles active status on click
/*$('.toggleActive').click(function() {
	resetAllActive();
	$(this).addClass('active');
});

// Function to clear all active instances
function resetAllActive(){
	$('.active').removeClass('active');
}

// OnClick functions for the side bar
$('#upload').click(function(){
	Content.loadXMLDoc("upload");
});

$('#new').click(function(){
	Content.loadXMLDoc("new");
});

$('#top').click(function(){
	Content.loadXMLDoc("top");
});

// SECTION - AJAX Functions

// AJAX call object for controlling the content in the main windows

var Content = {
	loadXMLDoc: function(path) {

		var xmlhttp;
		console.log("Attempting to access: " + document.URL + path);

		// Works for all modern browsers
		if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
		}else{// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}

		xmlhttp.onreadystatechange = function(){
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
				console.log("Accessed: " + document.URL + path)
				$("#content").html(xmlhttp.responseText);
			}
		}

		// ASync
		xmlhttp.open("GET", path, true);
		xmlhttp.send();

	}
}; */