# <div align="center">Banner Contact Merger</div>
#### <div align="center">Eric Kapalka  |  2024-06-08</div>

This application seeks to automate the tedious and error-prone process of merging contacts in Elucian Banner.  This is the n'th attempt at making such an application, and follows a different design pattern than previous attempts, employing Python only as a framework to hold together a collection of Javascript scripts that do the heavy lifting.  These scripts, provided they maintain the same inputs and outputs, can be updated instead of the Python application when the website changes, making this application more robust and easier to maintain.  Not to mention faster, as the Python application is only used to run the scripts, not to do the work itself.

The most important functions are in functions_general.py, which is a collection of general functions that are used in conjunction with the scripts in the c, r, and d folders.  Namely the functions extract_input_values and update_input_values, around which the entirety of this application is built.  These functions are used to extract and update the values of the input fields on the website, respectively.  Here is the gist of how they work:

## <div align="center">extract_input_values</div>

Before getting into how this works, you must understand the layout of the website first.  ALL input elements (be it text, date, or checkbox) have a corresponding label to explain what they are.  These elements are always wrapped in a `<div>` tag with a `data-widget` attribute of "textinput", "datefield", or "checkbox".  In the case of a datefield, the group also contains a date picker; in the case of a checkbox the group always contains a button.  So all possible element configurations to look for are the following:

```html
<div data-widget="textinput">
    <label>First Name</label>
    <input type="text" value="John">
    <!-- possibly other elements here -->
</div>
```

```html
<div data-widget="datefield">
    <label>Birthdate</label>
    <input type="text" value="01/01/2000">
    <button type="button" class="ui-datepicker-trigger"></button>
    <!-- possibly other elements here -->
</div>
```

```html
<input data-widget="checkbox">
    <label>Is Active</label>
    <input style="display: none;">
    <button type="button" role="checkbox"></button>
    <!-- possibly other elements here -->
</div>
```
So the process of extracting the values is as follows:

1. Identify all divs that contain a top-level label and input element that also have the `data-widget` attribute.
2. Filter this list of divs to VISIBLE elements only.
3. Build and return a dictionary with the following information:
```python
['label text': {
    'element': 'input or button element',
    'value': 'current value of input element'
},...]
```
The most important piece of this puzzle being that multiple elements with the same name will have increasingly high numbers appended to their names, e.g. 'First Name 1', 'First Name 2', etc.. This is done entirely in Javascript, so it takes an insignificant amount of time to run.  Because the element itself is returned, we don't have to re-identify the element when we want to update it, which saves a lot of time and complexity.  If we picked up an element that we aren't interested in, we can simply ignore it when we update the values; as long as we know the contextual name(s) of the element(s) we want to update (with the number if there are multiples), we can do so with ease.


## <div align="center">update_input_values</div>


Now that we have the elements themselves (returned from the function above), updating the values associated with them is trivial and simply a matter of working with the website to get the desired results.  `update_input_values` takes the element itself and desired value as input and does the following:

1. Identify the element's parent div.
2. Extract the parent div's `data-widget` attribute.
3. Interact with the element based on the `data-widget` attribute:
    - For `textinput` elements, set the value of the input element to the desired value. `datefield` elements are handled the same way, although some tricks are needed to keep the value from resetting.
    - For `checkbox` elements, click the button to toggle the checkbox.

Deciding what to update and what to delete is done by Python, but the actual updating is done by Javascript.  This allows for a more robust application that can be updated without having to change the Python application itself.

## <div align="center">The Rest</div>

The rest of the application is the framework holding the scripts together, the logic to decide what stays and what goes, and the "command queue" that is used to store and dish out commands.  The application runs on two threads -- a "Bad Worker" thread and a "Good Worker" thread, only interacting via the command queue.  The bad worker is assigned the GID ("**G**enerated **ID**", aka the Student ID) of the duplicate  / "bad" record and the good worker is assigned the GID of the destination / "good" record. The "Bad Worker" does the following:

1. Leaf through the forms on the duplicate record using Selenium and a handful of Javascript scripts and extract the values.  The forms and pages are always the same, although some may not contain relevant information.
2. Identify any pieces of information that should be reflected in the "Good Worker"'s record. 
3. Add these changes ("commands") into a SQLite database "command queue", where the "Bad Worker" is awaiting them to begin working.  The data in these commands is in the form of a JSON string for easy parsing.
4. If relevant, delete the data from the current (duplicate / "bad") record.
5. Continue for all fields on all forms.

"Good Worker":

1. Poll the command queue for any commands that are meant for it.  Eventually this application may support multiple workers of each type, but for now there is only one of each.  This structure makes it easy to add more workers if needed, though.
2. "Check out" the command and begin working on it.
3. Navigate to the form and tab specified in the command and add / update the values as specified.
4. "Check in" the command and move on to the next one, for all commands in the queue.  If there are no commands, the worker will wait until there are.

Finishing up:

1. Export the command queue to a CSV file for review.
