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
	game = new Satay(url, update);
}

var game = null;