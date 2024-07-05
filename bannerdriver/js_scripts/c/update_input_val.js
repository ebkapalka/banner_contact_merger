function updateInputValue(inputElement, newValue) {
    // Clear the input value
    inputElement.value = '';

    // Function to simulate typing each character
    function simulateTyping(input, value) {
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.blur();
    }

    // Function to simulate pressing Enter
    function simulateEnter(input) {
        var event = new KeyboardEvent('keydown', {
            bubbles: true,
            cancelable: true,
            key: 'Enter',
            code: 'Enter',
            keyCode: 13
        });
        input.dispatchEvent(event);
    }

    // Set the new value and simulate typing and pressing Enter
    simulateTyping(inputElement, newValue);
    simulateEnter(inputElement);

    return new Promise(function(resolve, reject) {
        var maxAttempts = 50;  // maximum number of polling attempts
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
        }, 100);  // polling interval in milliseconds
    });
}
