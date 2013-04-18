function Update () {
	$("#screen").attr('src', this.gamedata.curmap_imgsrc);
	$("#title").text(this.gamedata.curmap_name);
}

InitSatay(location.origin, Update);

game.AddAdditionalQueries(
	{
		"curmap": "imgsrc, name",
	}
);


$(document).keydown(function(e) {
	switch(e.keyCode) {
		// Up
		case 38:
			game.SendCommand('go', ['forward']);
			break;
		// Down
		case 40:
			game.SendCommand('go', ['backward']);
			break;

		// Left
		case 37:
			game.SendCommand('go', ['left']);
			break;

		// Right
		case 39:
			game.SendCommand('go', ['right']);
			break;

		default:
			break;
	}
});

$(document).ready(function() {
	game.GetData();
});