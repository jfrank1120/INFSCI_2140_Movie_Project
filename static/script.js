// CODE FOR XML REQUESTS - COURTESY OF PROF TIM JAMES THE REAL MVP OF PITT CS
function createXmlHttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!(xmlhttp)) {
        alert("Your browser does not support AJAX!");
    }
    return xmlhttp;
}

// this function converts a simple key-value object to a parameter string.
function objectToParameters(obj) {
    var text = '';
    for (var i in obj) {
        // encodeURIComponent is a built-in function that escapes to URL-safe values
        text += encodeURIComponent(i) + '=' + encodeURIComponent(obj[i]) + '&';
    }
    return text;
}


function postParameters(xmlHttp, target, parameters) {
    if (xmlHttp) {
        xmlHttp.open("POST", target, true); // XMLHttpRequest.open(method, url, async)
        var contentType = "application/x-www-form-urlencoded";
        xmlHttp.setRequestHeader("Content-type", contentType);
        xmlHttp.send(parameters);
    }
}

function sendJsonRequest(parameterObject, targetUrl, callbackFunction) {
    var xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var myObject = JSON.parse(xmlHttp.responseText);
            callbackFunction(myObject, targetUrl, parameterObject);
        }
    }
    postParameters(xmlHttp, targetUrl, objectToParameters(parameterObject));
}

function get(xmlHttp, target) {
    if (xmlHttp) {
        xmlHttp.open("GET", target, true); // XMLHttpRequest.open(method, url, async)
        var contentType = "application/x-www-form-urlencoded";
        xmlHttp.setRequestHeader("Content-type", contentType);
        xmlHttp.send();
    }
}

function sendGetRequest(targetUrl, callbackFunction) {
    var xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var myObject = JSON.parse(xmlHttp.responseText);
            callbackFunction(myObject, targetUrl);
        }
    }
    get(xmlHttp, targetUrl)
}

function getData(targetUrl, callbackFunction) {
    let xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            // note that you can check xmlHttp.status here for the HTTP response code
            try {
                let myObject = JSON.parse(xmlHttp.responseText);
                callbackFunction(myObject, targetUrl);
            } catch (exc) {
                console.log("There was a problem at the server.");
            }
        }
    }
    xmlHttp.open("GET", targetUrl, true);
    xmlHttp.send();
}

var fake_son = {}
function fake_callback() {}

// OTHER JAVASCRIPT CODE

function search() {
    var query = document.getElementById('query_field').value;
    console.log('Searching for : ' + query)
    var json_data = {
                       'query' : query
    };
    sendJsonRequest(json_data, '/search', populate_results)
}

function populate_results(results_data) {
    console.log(results_data)
    var results_area = document.getElementById('results_disp')
    for (var i = 0; i < results_data.length; i++) {
        // Create the list that shows the results
        var res = document.createElement("div");
        res.className = "result";
        var res_text = document.createElement("H5");
        //var title = results_data[i].split(',')
        //title = title[1].substring(1)
        var title_ex = results_data[i].replace(',', ':')
        res_text.innerText = title_ex;
        res.appendChild(res_text);
        results_area.appendChild(res);
    }
    console.log('APPENDED ALL RESULTS')
}

//Javascript Document//
function checkform(){
	var name = document.getElementById("name").value;
	var email = document.getElementById("email").value;
	var message = document.getElementById("message").value;
	var mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	
	if (name.length<3){
		alert("Name should be more than two letters!");
		return false;
	}
	else if (!email.match(mailformat)){
		alert("Entered email address is invalid!");
		return false;
	}
	else if(message.length<20){
		alert("Message should be more than 20 characters!");
		return false;
	}
	else{
		return true;
	}
}

function validate()
{
	//get the values
	var name = document.getElementById("mname").value;
	var year = document.getElementById("year").value;
	var genre = document.getElementById("genre").value;
	var description = document.getElementById("description").value;
	var email = document.getElementById("email").value;
	var poster = document.getElementById("poster").value;
	var agree = document.getElementById("agree").checked;
	var mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	
	//name validation
	if (name==""){
		alert("Name is Missing!");
		return false;
	}
	else if(name.length<2)
		{
			alert("Name must contain more than 2 characters!");
			return false;
		}
	
	//year validation
	else if (year==""){
		alert("Year is Missing!");
		return false;
	}
	else if((year.length<4) || (year.length>4))
		{
			alert("Year must contain 4 Numbers!");
			return false;
		}
	else if (isNaN(year))
		{
			alert("Year must be in numeric form!");
			return false;
		}
	
	//genre validation
	else if (genre==""){
		alert("Genre isn't selected!");
		return false;
	}
	
	//description validation
	else if (description==""){
		alert("Description is Missing!");
		return false;
	}
	else if(description.length<30)
		{
			alert("Description is too short!");
			return false;
		}
	else if(description.length>250)
		{
			alert("Maximum description limit (250) exceeded!");
			return false;
		}

	//email validation
	else if (email==""){
		alert("Email is Missing!");
		return false;
	}
	else if (!email.match(mailformat))
		{
			alert("Email is not valid!");
			return false;
		}
	
	//poster validation
	else if(poster==""){
		alert("poster is missing or invalid!");
		return false;
	}

	//agree validation
	else if (agree!=true){
		alert("You haven't agreed to the terms!");
		return false;
	}
	else
		{
			return true;
		}
}

