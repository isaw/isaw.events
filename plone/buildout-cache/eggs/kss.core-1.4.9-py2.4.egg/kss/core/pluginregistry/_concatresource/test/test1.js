
_PythonKw = function(kw) {
	this.kw = kw;
	}

_PythonKw.prototype.toJSON = function() {
	var pack = {"pythonKwMaRkEr": this.kw};
	return toJSON(pack);
	}
	
function PythonKw(kw) {
	return new _PythonKw(kw);
	}
