// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, function(tabs) {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}

function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
	var page = "";
	
	var range = document.getElementById('sentiment');
	var val = document.getElementById('value');
	var rate = document.getElementById('rate');
	var r2d2 = document.getElementById('r2d2');
	
	range.oninput = function(){
		renderStatus('Rate the Sentiment of this Page');
		val.innerHTML = range.value;
	}
	
	r2d2.onclick = function(){
		var xhttp = new XMLHttpRequest();
		var url = 'http://127.0.0.1:8000';
		var params = 'url=' + page;
		xhttp.open('GET', url + "?" + params, true);
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhttp.onreadystatechange = function() {//Call a function when the state changes.
			if(xhttp.readyState == 4 && xhttp.status == 200) {
				console.log(xhttp.responseText);
				renderStatus('R2D2 rates this page a: ' +  xhttp.responseText);
			}else{
				renderStatus('R2D2 is currently malfunctioning.');
			}
		}
		xhttp.send();
	}
	
	rate.onclick = function(){
		var xhttp = new XMLHttpRequest();
		var url = 'http://127.0.0.1:8000';
		var params = 'url=' + page + '&rating=' + val.innerHTML;
		xhttp.open('POST', url, true);
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhttp.onreadystatechange = function() {//Call a function when the state changes.
			if(xhttp.readyState == 4 && xhttp.status == 200) {
				console.log(xhttp.responseText);
			}
		}
		xhttp.send(params);
		renderStatus('Thanks! Goto/R2D2 for details!');
		range.style.display='none';
		val.style.display='none';
		rate.style.display='none';
	}
	
  getCurrentTabUrl(function(url) {
    renderStatus('Rate the Sentiment of this Page');
	page = url;
  });
});
