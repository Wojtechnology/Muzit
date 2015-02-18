// JavaScript :: Controller
// Author: Wojtek Swiderski
// Main data controller for the website

// SECTION - JQuery Functions
$(document).ready(function(){
	// Returns cookie name for AJAX request
	function getCookie(name) {
		var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
		return c ? c[1] : undefined;
	}

	// Clears the upvote and downvote buttons for given element
	function clearClassVote(parent){
		parent.find('.upButton').removeClass('orangeVote');
		parent.find('.downButton').removeClass('blueVote');
	}

	// Makes AJAX request to upvote or downvote
	function vote(parent, type){
		userID = parent.find('.userID').val();
		$.post('vote?type=' + type + '&userID=' + userID + '&_xsrf=' + getCookie('_xsrf'), function(data){});
	}

	$('.upButton').click(function(){
		clearClassVote($(this).parent('span'));
		$(this).addClass('orangeVote');
		vote($(this).parent('span'), 'up');
	});
	$('.downButton').click(function(){
		clearClassVote($(this).parent('span'));
		$(this).addClass('blueVote');
		vote($(this).parent('span'), 'down');
	});
});