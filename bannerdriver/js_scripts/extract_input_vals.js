function extractInputValues() {
    function isVisible(element) {
        var style = window.getComputedStyle(element);
        return style && style.display !== 'none' && style.visibility !== 'hidden' && element.offsetWidth > 0 && element.offsetHeight > 0;
    }

    var divs = document.querySelectorAll('div[data-widget="textinput"], div[data-widget="datefield"], div[data-widget="checkbox"]');
    var data = {};
    var labelCount = {};

    divs.forEach(function(div) {
        if (isVisible(div)) {
            var label = div.querySelector(':scope > label');
            var input = div.querySelector(':scope > input');
            if (label && input) {
                var labelText = label.innerText.trim();
                if (labelCount[labelText] === undefined) {
                    labelCount[labelText] = 0;
                }
                labelCount[labelText]++;
                var labelKey = labelText;
                if (labelCount[labelText] > 1) {
                    labelKey = labelText + '_' + labelCount[labelText];
                }
                var inputValue;
                if (div.getAttribute('data-widget') === 'checkbox') {
                    inputValue = input.checked ? 'checked' : 'unchecked';
                } else {
                    inputValue = input.value;
                }
                data[labelKey] = {element: input, value: inputValue};
            }
        }
    });
    return data;
}
