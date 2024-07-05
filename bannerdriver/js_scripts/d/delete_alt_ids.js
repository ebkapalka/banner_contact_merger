(function() {
    function clickElement(selector, context = document) {
        var element = context.querySelector(selector);
        if (element) {
            element.click();
            return true;
        }
        return false;
    }

    function deleteRecord(iframeDocument) {
        var deleteBtn = iframeDocument.querySelector('a[data-action="DELETE_RECORD"]:not([aria-disabled="true"])');
        if (deleteBtn) {
            deleteBtn.click();
            setTimeout(() => confirmDeletion(iframeDocument), 500);  // Adjust the delay if needed
        } else {
            console.log('No more records to delete or delete button not found.');
        }
    }

    function confirmDeletion(iframeDocument) {
        var confirmBtn = Array.from(iframeDocument.querySelectorAll('button.btn-primary')).find(btn => btn.textContent.trim() === 'Continue');
        if (confirmBtn) {
            confirmBtn.click();
            setTimeout(() => deleteRecord(iframeDocument), 500);  // Adjust the delay if needed
        } else {
            console.log('Continue button not found or no more deletion confirmation.');
        }
    }

    function startProcess(iframeDocument) {
        console.log('Attempting to click the tab...');
        if (clickElement('#tabGIdenTabCanvas_tab1', iframeDocument)) {
            console.log('Tab clicked successfully.');
            setTimeout(() => deleteRecord(iframeDocument), 500);  // Adjust the delay if needed
        } else {
            console.log('Tab not found.');
        }
    }

    function switchToIframe() {
        var iframe = document.getElementById('bannerHS');
        if (iframe) {
            console.log('Switching to iframe...');
            var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
            iframe.contentWindow.focus();
            console.log('Switched to iframe.');
            startProcess(iframeDocument);
        } else {
            console.log('iFrame not found.');
        }
    }

    switchToIframe();
})();
