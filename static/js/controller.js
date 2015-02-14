// Toggles active status on click
$('.toggleActive').click(function() {
	resetAllActive();
	$(this).addClass('active');
});

// Function to clear all active instances
function resetAllActive(){
	$('.active').removeClass('active');
}