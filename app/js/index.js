function generateSearchForm()
{
	var seeker = $("#dropa").find(":selected").text();
	var target = $("#dropb").find(":selected").text();
	form = ""
	form += "<form action='search' method='post'>";
	form += "<input type='hidden' value='"+seeker+"' name='seeker'></input>";
	form += "<input type='hidden' value='"+target+"' name='target'></input>";
	
	form += $("#halfform").html();
	
	form += "</form>";
	return form;
}

function updateDropdown(target)
{
	var off = "";
	if ($("#drop"+target).find(":selected").text() == "Artist")
		off = "n";
	$("#a"+target).text("a"+off);
}

function setup()
{
	$("#background").click(function() {
		$("#background").fadeOut();
		$("#popup").fadeOut();
		$("#popup2").fadeOut();
		$("#popup3").fadeOut();
	});
	
	if ($(".notice").length != 0)
		$(".notice").delay(2000).fadeOut();
}

function popup2()
{
	$("#background").fadeIn();
	$("#popup2").fadeIn();
}

function popup3()
{
	$("#background").fadeIn();
	$("#popup3").fadeIn();
}

function popup()
{
	$("#background").fadeIn();
	$("#popup").html(generateSearchForm());
	$("#popup").fadeIn();
	
}

