var modal = document.getElementById("hiddenMenu");
var popupButton = document.getElementById("popupButton");
var closeButton = document.getElementsByClassName("close")[0];
var mask = document.getElementById('mask');
let search_values_obj = {};
let final_search;

//handling check boxes in popup
document.getElementById("y-fire").addEventListener('click', function () {
    if (this.checked) {
        document.getElementById("campfire_checkbx").innerHTML = 'Yes';
    } else {
        document.getElementById("campfire_checkbx").innerHTML = 'No';
    }
})

document.getElementById("y-pets").addEventListener('click', function () {
    if (this.checked) {
        document.getElementById("pets_checkbx").innerHTML = 'Yes';
    } else {
        document.getElementById("pets_checkbx").innerHTML = 'No';
    }
})

function clear_modal() {
    let elements = document.getElementById('popupFormElements').elements;

    for (let i = 0; i < elements.length; i++) {
        var item = elements.item(i);

        if (item.type === "checkbox") {
            document.getElementById("campfire_checkbx").innerHTML = 'Y/n';
            document.getElementById("pets_checkbx").innerHTML = 'Y/n';
            elements[i].checked = false;
        } else {
            elements[i].value = '';
        }
    }
}

//logic for bringing up the popup search, if searched then it says Clear Search
popupButton.addEventListener('click', function () {
    if (searched) {
        this.innerHTML = 'Click To Find Your Campsite!';
        searchQuery = campQuery;
        searched = false;
        map.removeControl(editSearch);
        map.addControl(drawControl);
        drawnItems.clearLayers();
        activeBox = false;
        boxBounds = '';
        addCampsites(searchQuery, true);
    } else {
        modal.style.display = "block";
        mask.style.display = "block";
    }
})

closeButton.addEventListener('click', function () {
    modal.style.display = "none";
    mask.style.display = "none";
    clear_modal();
})

window.addEventListener('click', function (e) {
    if (e.target == mask) {
        modal.style.display = "none";
        mask.style.display = "none";
        clear_modal();
    }
})

//stores all the values from the popup from into an array instead of an object
let searchFunction = function (values_obj) {
    final_search = [];
    Object.keys(values_obj).forEach(function (key) {
        if (values_obj[key]) {
            final_search.push(key, values_obj[key]);
        }
    })
};

//builds the query based off of final search array, I was more comfortable using an array instead of an object at the time
function buildQuery(attributes_list) {
    let counter = false;
    for (let i = 0; i < attributes_list.length; i += 2) {
        if (!counter) {
            if (attributes_list[i] === 'pets_allowed') {
                if (attributes_list[i + 1] === " = 'No'") {
                    searchQuery += ' WHERE ' + attributes_list[i] + attributes_list[i + 1];
                } else {
                    searchQuery += ' WHERE (' + attributes_list[i] + attributes_list[i + 1];
                }
            } else {
                searchQuery += ' WHERE ' + attributes_list[i] + attributes_list[i + 1];
            }
        } else {
            if (attributes_list[i] === 'pets_allowed') {
                if (attributes_list[i + 1] === " = 'No'") {
                    searchQuery += ' AND ' + attributes_list[i] + attributes_list[i + 1];
                } else {
                    searchQuery += ' AND (' + attributes_list[i] + attributes_list[i + 1];
                }
            } else {
                searchQuery += ' AND ' + attributes_list[i] + attributes_list[i + 1];
            }
        }
        counter = true;
    }
}

//handling submit of popup
let submit = document.getElementById('popupQuerySubmit');
submit.addEventListener('click', (e) => {
    e.preventDefault()
    let elements = document.getElementById('popupFormElements').elements;
    for (let i = 0; i < elements.length; i++) {
        var item = elements.item(i);
        //checkbox logic, if checked means yes, if clicked again means no, if no click not added to query
        if (item.type === "checkbox") {
            if (item.checked === true) {
                if (item.name === "campfire_allowed") {
                    search_values_obj[item.name] = " = 'Yes'";
                } else if (item.name === "pets_allowed") {
                    search_values_obj[item.name] = " = 'Yes' OR " + item.name + " = 'Domestic,Horse' OR " + item.name + " = 'Pets Allowed')";
                }
                elements[i].checked = false;
                document.getElementById("campfire_checkbx").innerHTML = 'Y/n';
                document.getElementById("pets_checkbx").innerHTML = 'Y/n';
            } else if (item.previousSibling.innerHTML === 'No') {
                search_values_obj[item.name] = " = 'No'";
                document.getElementById("campfire_checkbx").innerHTML = 'Y/n';
                document.getElementById("pets_checkbx").innerHTML = 'Y/n';
            } else {
                search_values_obj[item.name] = '';
            }

        } else {
            search_values_obj[item.name] = item.value;
            elements[i].value = '';
        }
    };
    modal.style.display = "none";
    mask.style.display = "none";
    searchFunction(search_values_obj);
    buildQuery(final_search);
    //error handling, if the user doesnt choose anything but sumbits
    if (final_search.length > 0) {
        searched = true;
        popupButton.innerHTML = 'Clear search';
        //if there is already a user drawn box, then the boxbounds are added to a temp query in case user clears box after searching
        if (activeBox) {
            let tempQuery = searchQuery + boxBounds;
            addCampsites(tempQuery, true);
        } else {
            addCampsites(searchQuery, true);
        }
    } else {
        searched = false;
    }
});