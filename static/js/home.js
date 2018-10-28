/* Present Day in select tag */

var today = document.getElementsByTagName('option')[0];
let dot = new Date();
let day = new Date().getDay();
let _day;
switch (true) {
    case day == 0:
        _day = 'Sun';
        break
    case day == 1:
        _day = 'Mon';
        break
    case day == 2:
        _day = 'Tue';
        break
    case day == 3:
        _day = 'Wed';
        break
    case day == 4:
        _day = 'Thu';
        break
    case day == 5:
        _day = 'Fri';
        break
    case day == 6:
        _day = 'Sat';
        break
};
today.innerHTML = `Today, ${_day} ${dot.getMonth()+1}/${dot.getDate()}/${dot.getFullYear()}`;
today.setAttribute('value', today.innerHTML);

/* Disable Return key */

var deactivateReturnKey = function (event) {
    if (event.keyCode == 13) {
        return false;
    };
};

document.onkeydown = deactivateReturnKey;

/* XMLHttpRequest */

// Remove Item

function ajaxRemove(event) {
    var delrequest = new XMLHttpRequest();


    var conCat = document.getElementById("conCat");
    
    var information = event.target.parentNode.parentNode.children[1].children[0].innerHTML
    
    let deleteItems = document.getElementsByClassName('remove')
    let index = Array.from(deleteItems).indexOf(event.target);
    let removal = deleteItems[index].parentNode.parentNode;
    conCat.removeChild(removal);

    delrequest.open("DELETE", '/', true);
    delrequest.setRequestHeader("Content-type", "/x-www-form-urlencoded");
    delrequest.send(information);
}

// Add Item 

function ajaxAdd(url, content) {
    var addrequest = new XMLHttpRequest();
    addrequest.onload = function () {
        if (this.readyState == 4 && this.status == 200) {
            var conCat = document.getElementById("conCat");

            var divRow, divcol4, divcol8, buttonDel, textArea;

            var responseInfo = this.responseText;

            divRow = document.createElement('DIV');
            divcol4 = document.createElement('DIV');
            divcol8 = document.createElement('DIV');
            textArea = document.createElement('textarea');
            form = document.createElement('form');
            buttonDel = document.createElement('button');


            buttonDel.setAttribute("class", "btn btn-danger remove");

            buttonDel.innerHTML = '-';
            buttonDel.setAttribute('onclick', "ajaxRemove(event)");

            divRow.setAttribute("class", "row");

            divcol4.setAttribute("class", "col-4");

            divcol8.setAttribute("class", "col-8");

            if (responseInfo.length > 50) {
                textArea.setAttribute("class", "changeBgc");
                textArea.setAttribute("name", "embedded");
                textArea.setAttribute("cols", "50");
                textArea.setAttribute("rows", "3");
                textArea.readOnly = true;
                textArea.innerHTML = responseInfo;
            } else {
                textArea.setAttribute("class", "changeBgc");
                textArea.setAttribute("name", "embedded");
                textArea.setAttribute("cols", String(responseInfo.length));
                textArea.setAttribute("rows", "2");
                textArea.readOnly = true;
                textArea.innerHTML = responseInfo;
            }

            divcol8.appendChild(textArea);
            divcol4.appendChild(buttonDel);
            divRow.appendChild(divcol4);
            divRow.appendChild(divcol8);

            conCat.appendChild(divRow);
            begin();
            identifier();
        }
    };
    addrequest.open("POST", url, true);
    addrequest.setRequestHeader("Content-type", url + "x-www-form-urlencoded");
    addrequest.send(content);

};





/* Create an addition of post button and form on landing */

function begin() {
    // save and cancel buttons with input embedded in form tag
    var div1, div2, button1, button2, input1;

    var conCat = document.getElementById("conCat");

    div1 = document.createElement('DIV');
    div1.setAttribute("class", "input-group mb-3");
    div2 = document.createElement('DIV');
    div2.setAttribute("class", "input-group-prepend");
    div1.id = "button-addon3"
    button1 = document.createElement('button')
    button1.setAttribute("class", "btn btn-success save");

    button1.innerHTML = 'Save';
    button2 = document.createElement('button');
    button2.setAttribute("class", "btn btn-danger cancel");
    button2.setAttribute("type", "button");
    button2.innerHTML = 'Cancel';
    input1 = document.createElement('input');
    input1.setAttribute("type", "text");
    input1.setAttribute("class", "form-control");
    input1.setAttribute("maxlength", "100");
    input1.setAttribute("name", "items");
    div2.appendChild(button1);
    div2.appendChild(button2);
    div1.appendChild(div2);
    div1.appendChild(input1);
    
    // plus sign Button 
    var rowDiv = document.createElement('DIV');
    rowDiv.setAttribute("class", "row");
    var colDiv1 = document.createElement('DIV');
    colDiv1.setAttribute("class", "col-4");
    var colDiv2 = document.createElement('DIV');
    colDiv2.setAttribute("class", "col-8");
    var button = document.createElement('button');
    button.setAttribute("class", "btn btn-success add");
    button.setAttribute("type", "button");
    button.innerHTML = '+';
    let form = document.createElement('form');
    form.setAttribute('method', 'POST');
    form.id = 'invisible';
    form.addEventListener("submit", form_handler);

    function form_handler(event) {
        if (input1.value.length > 0) {
            event.preventDefault();
            let forms = document.getElementsByTagName('form')
            let index = Array.from(forms).indexOf(event.target);
            let form1 = forms[index].parentNode.parentNode;
            conCat.removeChild(form1)
            ajaxAdd('/', input1.value);
        }
    };

    form.appendChild(div1);
    colDiv1.appendChild(button);
    colDiv2.appendChild(form);
    rowDiv.appendChild(colDiv1);
    rowDiv.appendChild(colDiv2)
    conCat.appendChild(rowDiv);

};

/* Adding Functionality to buttons: plus and minus signs, save, and cancel buttons with recursion */

function identifier() {
    var buttons = document.getElementsByTagName('button');
    var addButns = document.getElementsByClassName('add');
    var formCancel = document.getElementsByClassName('cancel');
    for (var i = 0; i < buttons.length; i++) {
        if (Array.from(addButns).includes(buttons[i])) {
            // Remove "invisible" id from form to make display visible
            buttons[i].onclick = function (event) {
                var index = Array.from(addButns).indexOf(event.target);
                var space = addButns[index].parentNode.parentElement.children[1].firstChild
                if (space.id == 'invisible') {
                    space.removeAttribute("id");
                }
            };
        } else if (Array.from(formCancel).includes(buttons[i])) {
            buttons[i].onclick = function (event) {
                // Assign "invisible" id to form to make display:none again
                let index = Array.from(formCancel).indexOf(event.target);
                let form = formCancel[index].parentNode.parentNode.parentNode;
                form.setAttribute('id', 'invisible');
            }
        }
    };
};




/* Run Functions */

begin();
identifier();
