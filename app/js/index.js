function generateSearchForm()
{
	var seeker = "", target="";
	form = "<form>";
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

