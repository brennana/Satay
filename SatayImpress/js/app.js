if ("ontouchstart" in document.documentElement) { 
    document.querySelector(".hint").innerHTML = "<p>Tap on the left or right to navigate</p>";
}

if ( $(".impress-not-supported").length == 0)
{
	$(document).on("keyup ready", function(e){
		$(".block").each( function(index, element){
			if ($(this).children(".active").length == 0) {
				$(this).removeClass("active");
			}
			else {
				$(this).addClass("active");
			}
		});
	});
}
else {
	$(".block").addClass("active");
	$(".main").addClass("active");
}