// Satay.js -- A js interface for Satay.

function Satay(url, update) {
	this.url = url;
	this.gamedata = {};

	if (typeof(update) == "function") {
		this.update = update;
	}
	else {
		throw new TypeError("update argument must be a function!")
	}
	return this;
}

Satay.prototype.AddAdditionalQueries = function(queries, single_query) {
	if (typeof queries == "object") {
		this.additionalQueries = queries;
	}
	else {
		this.additionalQueries[queries] = single_query;
	}
};

Satay.prototype.SendCommand = function(command, arguments) {
	args = "";
	for (var i = 0; i < arguments.length; i++) {
		args += '/' + arguments[i];
	}

	$.getJSON(this.url+'/'+command+args, this.additionalQueries, SendCommandCallback);
};

Satay.prototype.GetData = function() {
	$.getJSON(this.url+'/dataonly', this.additionalQueries, SendCommandCallback);
};

function SendCommandCallback(data, textStatus, jqXHR) {
	if (data.status) {
		game.gamedata = data.gameData;
		game.update();
	}
}

function GetPropertyCallback(data, textStatus, jqXHR) {
	game.lastProperty = data.value;
}

function InitSatay(url, update) {
	// Get new session ID and always send to server in AJAX
	if(ReadCookie("satay_session") == null) {
		$.get(url+'/session');
	}
	game = new Satay(url, update);
}


// Cookie functions
function CreateCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function ReadCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function EraseCookie(name) {
	createCookie(name,"",-1);
}

var game = null;