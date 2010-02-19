



dojo.require("dojo.widget.Select");

function init(nid, nlabel, nvalue) {
	if(nlabel =='' && nvalue == ''){
	nlabel=' ';
	nvalue=' ';
}

  dojo.widget.byId(nid).setLabel(nlabel);
  dojo.widget.byId(nid).setValue(nvalue);
}