chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);

		chrome.runtime.sendMessage({greeting: "test"}, function(response) {});

	}
	}, 10);
});
