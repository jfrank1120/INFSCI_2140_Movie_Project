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
    var buttons = document.getElementsByTagName('input');
    var year_data = validate_year()
    if (year_data.length == 0) {
        var year_field = document.getElementById("year")
        year_field.value = ""
    }
    var filters = {};
    for (var ind = 0; ind < buttons.length; ind++) {
        if (buttons[ind].type == "checkbox") {
            filters[buttons[ind].id] = buttons[ind].checked
        }
    }
    console.log('Searching for : ' + query)
    var json_data = {
                       'query' : query,
                       'filters' : JSON.stringify(filters),
                       'year': year_data
    };
    sendJsonRequest(json_data, '/search', populate_results)
}

function populate_results(results_data) {
    console.log(results_data)
    var results_area = document.getElementById('results_disp')
    // Clear all children on new search
    while (results_area.firstChild) {
        results_area.removeChild(results_area.firstChild)
    }
    if (results_data.length == 0) {
        var res = document.createElement("div");
        res.className = "result";
        var res_text = document.createElement("H5");
        res_text.innerText = "No Results Found";
        res.appendChild(res_text);
        results_area.appendChild(res);
    } else {
        for (var i = 0; i < results_data.length; i++) {
            // Create the list that shows the results
            var res = document.createElement("div");
            res.className = "result";
            var res_text = document.createElement("H5");
            var title_ex = results_data[i].replace(',', ':')
            res_text.setAttribute("onclick", "get_similar('" + title_ex + "');")
            //var title = results_data[i].split(',')
            //title = title[1].substring(1)
            res_text.innerText = title_ex;
            res.appendChild(res_text);
            results_area.appendChild(res);
        }
    }
}

function get_similar(movie_title) {
    console.log('Getting similar: ' + movie_title)
    movie_json = {
        'movie_title' : movie_title
    }
    sendJsonRequest(movie_json, '/get_similar', send_to_page)
}

function send_to_page(results_list) {
    window.location.href = 'movies_similar.html'
}

// cheeky way to get the data from the session
function get_res_sim_data() {
    sendJsonRequest(fake_son, '/get_similar_results', populate_similar)
}

function populate_similar(results_data) {
    console.log(results_data)
    var movie_title_text = document.getElementById('selected_movie');
    movie_title_text.innerText = 'Movies Similar to: ' + results_data['movie_title']
    results_data = results_data['similar_results']
    var results_area = document.getElementById('similar_results')
    for (var i = 0; i < results_data.length; i++) {
        // Create the list that shows the results
        var res = document.createElement("div");
        res.className = "result";
        res.className = "d-flex"
        var res_text = document.createElement("H5");
        var title_ex = results_data[i].replace(',', ':')
        res_text.setAttribute("onclick", "get_similar('" + title_ex + "');")
        res_text.innerText = title_ex;
        res.appendChild(res_text);
        results_area.appendChild(res);
    }
}

function get_recs() {
    sendJsonRequest(fake_son, '/get_recs', populate_recs)
}

function populate_recs(results_data) {
    console.log(results_data)
    var results_area = document.getElementById('rec_results')
    if (results_data.length == 0) {
        var res = document.createElement("div");
        res.className = "result";
        var res_text = document.createElement("H4");
        res_text.innerText = "No searches to use";
        res.appendChild(res_text);
        results_area.appendChild(res);
    }
    for (var i = 0; i < results_data.length; i++) {
        // Create the list that shows the results
        var res = document.createElement("div");
        res.className = "result";
        res.className = "d-flex"
        var res_text = document.createElement("H5");
        var title_ex = results_data[i].replace(',', ':')
        res_text.setAttribute("onclick", "get_similar('" + title_ex + "');")
        res_text.innerText = title_ex;
        res.appendChild(res_text);
        results_area.appendChild(res);
    }
}

function validate_year() {
	var year = document.getElementById("year").value;
	//year validation
	if (year==""){
		return "";
	}
	else if((year.length<4) || (year.length>4)) {
        return "";
	}
	else if (isNaN(year)) {
        return "";
	} else if (parseInt(year) > 1901 && parseInt(year) < 2017) {
	    return year;
	}
}

