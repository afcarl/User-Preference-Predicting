var page = require('webpage').create();
var args = require('system').args;
var url = args[1]
//for (var k=1; k<3;k++){
// 	console.log(url[k])
page.open(url, function (status) {
if (status !== 'success') {
    console.log('Unable to load the address!');
} 
else {	
		console.log(url)
        var kk = page.evaluate(function () { 
        var bb = document.querySelectorAll('.result, .result-op');
        var rect = []
        for (var i=0; i <bb.length; i++){
        	rect[i] = bb[i].getBoundingClientRect()
        }
        return rect
    	});
       	
       	for (var i=0 ; i<kk.length; i++){
        	console.log(kk[i].height)
        	page.clipRect = {
            top:    kk[i].top,
            left:   kk[i].left,
            width:  kk[i].width,
            height: kk[i].height
			 };
        	page.render("capture_result"+i.toString()+".png");
        }
        console.log("***")
		 phantom.exit(); 
		 }
});

//}


  	
/*
var page = require('webpage').create();

page.open("./2.html", function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
    } else {
            page.onError(function (msg, trace) { 
                var bb = $(".capture")[0];
                console.log(bb);
                console.log(bb.getBoundingClientRect().height);
                for (var i=0 ; i<bb.length; i++)
                {
                	var rect = bb[i].getBoundingClientRect();
                	console.log(rect.height)
                }


            });
    }
    phantom.exit();
});
*/