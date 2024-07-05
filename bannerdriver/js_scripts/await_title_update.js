function waitForTitleUpdate(inputElement, newValue) {
    return new Promise(function(resolve, reject) {
        var maxAttempts = 50;
        var attempts = 0;
        var interval = setInterval(function() {
            if (inputElement.title === newValue) {
                clearInterval(interval);
                resolve();
            }
            attempts++;
            if (attempts >= maxAttempts) {
                clearInterval(interval);
                reject(new Error("Title attribute did not update"));
            }
        }, 100);
    });
}
