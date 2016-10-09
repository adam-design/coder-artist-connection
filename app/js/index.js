function generateSearchForm()
{
	var seeker = $("#dropa").find(":selected").text();
	var target = $("#dropb").find(":selected").text();
	form = "<h1>What kind of artist?</h1>";
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
	});
}

function popup()
{
	$("#background").fadeIn();
	$("#popup").html(generateSearchForm());
	$("#popup").fadeIn();
	
}
