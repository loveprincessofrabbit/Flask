
function checkText(el, text){
	if(el.value == text){
		el.value = "";
	}else
	if(el.value == ""){
		el.value = text;
	}
}

window.document.onload = function(e){loadElClassName();}
window.onload = function(e){loadElClassName();}

function loadElClassName(){
	if (document.getElementsByClassName == undefined) {
		document.getElementsByClassName = function(className)
		{
			var hasClassName = new RegExp("(?:^|\\s)" + className + "(?:$|\\s)");
			var allElements = document.getElementsByTagName("*");
			var results = [];

			var element;
			for (var i = 0; (element = allElements[i]) != null; i++) {
				var elementClass = element.className;
				if (elementClass && elementClass.indexOf(className) != -1 && hasClassName.test(elementClass))
					results.push(element);
			}

			return results;
		}
	}
}

function switchTab(element){
	attribs = document.getElementsByClassName("active")[0].attributes;
	for(n = 0;n<=attribs.length;n++){
		if(document.getElementsByClassName("active")[0].attributes[n].name == "name"){
			var thihide = document.getElementsByClassName("active")[0].attributes[n].value;
			break;
		}
	}
	
	attribz = element.attributes;
	for(n = 0;n<=attribz.length;n++){
		if(element.attributes[n].name == "name"){
			var thisdisplay = element.attributes[n].value;
			break;
		}
	}
	thihide = "tab-"+thihide;
	thisdisplay = "tab-"+thisdisplay;
	if(thihide == thisdisplay)return;
	fadeOut(thihide, thisdisplay, 100);
	document.getElementsByClassName("active")[0].className = null;
	element.className = "active";
}

function setOpacity(e,opacity){
	if(!e)return;
	if(opacity ==5)e.style.display = "block";
	var o=e.style;
	o.opacity=(opacity/100);
	o.MozOpacity=(opacity/100);
	o.KhtmlOpacity=(opacity/100);
	o.filter="alpha(opacity="+opacity+")";
}

function fadeOut(elid, noid, opac){
	if(!elid && !document.getElementById(elid))return;
	if(opac <= 0){
		document.getElementById(elid).style.display = "none";
		fadeIn(noid, 0);
		return;
	}
	opac = opac-5;
	setOpacity(document.getElementById(elid), opac);
	setTimeout("fadeOut('"+elid+"', '"+noid+"', "+opac+")", 10);
}

function fadeIn(elid, opac){
	if(opac >= 100)return;
	opac = opac+5;
	setOpacity(document.getElementById(elid), opac);
	setTimeout("fadeIn('"+elid+"', "+opac+")", 10);
}

function showVideo(element){
	attribz = element.attributes;
	for(n = 0;n<=attribz.length;n++){
		if(element.attributes[n].name == "name"){
			var elname = element.attributes[n].value;
			break;
		}
	}
	document.getElementById(elname+'-image').style.display = 'none';
	document.getElementById(elname+'-video').style.display = 'block';
}

$(document).ready(function() {
		var n = $("#carousel_ul li").length;

        $('#right_scroll').click(function(){
			var z = parseInt($('#carousel_ul').css('left'));
			if(((z*(-1)+625) >= $('#carousel_ul li').outerWidth()*(n)) )return;
            var item_width = $('#carousel_ul li').outerWidth()*5;
            var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;
            $('#carousel_ul').animate({'left' : left_indent},{queue:false, duration:500},function(){
                $('#carousel_ul li:last').after($('#carousel_ul li:first'));
                $('#carousel_ul').css({'left' : '-625px'});
            });
        });

        $('#left_scroll').click(function(){
			var z = parseInt($('#carousel_ul').css('left'));
			if(z == 0)return;
            var item_width = $('#carousel_ul li').outerWidth()*5;
            var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;
            $('#carousel_ul').animate({'left' : left_indent},{queue:false, duration:500},function(){
            $('#carousel_ul li:first').before($('#carousel_ul li:last'));
            $('#carousel_ul').css({'left' : '-625px'});
            });

        });
  });