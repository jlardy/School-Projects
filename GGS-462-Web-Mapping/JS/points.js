// div for campsite cards
let cardsList = document.querySelector(".items");


//MarkerClusterGroup that collects all POI GeoJSON objects
var lakes_group = new L.markerClusterGroup().addTo(map);
var campsites_group = new L.markerClusterGroup().addTo(map);


// lakes function
let lakesQuery = "https://jlardy.carto.com/api/v2/sql?format=GeoJSON&q=SELECT * FROM fishinglakes";

function addLakes() {
  $.getJSON(lakesQuery, function (data) {
    lake_objects = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        // add popup with info
        layer.bindPopup("<h2>" + feature.properties.name + "</p>");
      },
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
      }
    });
    lake_objects.addTo(lakes_group);
  });
};
addLakes();


let campQuery = "https://jlardy.carto.com/api/v2/sql?format=GeoJSON&q=SELECT * FROM campsite_data";
let searchQuery = campQuery;
let disableClicking = document.getElementById('zoomingMask');

// clicking a card on the right hand side of the page zooms to it, even with search queries in place
function zoomToFeature(e) {
  let to_lat, to_long
  let zoom = 16
  disableClicking.style.display = "block"
  if (e.srcElement.parentElement.children.length === 3) {
    to_lat = Number(e.srcElement.parentElement.children[0].innerHTML);
    to_long = Number(e.srcElement.parentElement.children[1].innerHTML);
  } else if (e.target.childNodes.length === 4) {
    to_lat = Number(e.target.childNodes[0].innerHTML);
    to_long = Number(e.target.childNodes[2].innerHTML);
  }
  lakes_group.removeLayer(lake_objects);
  campsites_group.removeLayer(campsites);
  map.flyTo([to_lat, to_long], zoom);
  map.once('zoomend', function () {
    if (searched && activeBox) {
      let tempQuery = searchQuery + boxBounds;
      addCampsites(tempQuery, false, zoom);
    } else if (activeBox) {
      addCampsites(finalBoxQuery, false, zoom);
    } else if (searched) {
      addCampsites(searchQuery, false, zoom);
    } else {
      addCampsites(campQuery, false, zoom);
    }
    addLakes();
    disableClicking.style.display = 'none';
  });
};

// function to add campsites, option parameters to clear the layer before adding it and if it needs to be zoomed
// multi sites variable checks to see if the returned query is empty
let multi_sites = true;

function addCampsites(query, remove, zoom) {
  if (!multi_sites) {
    alert('Your search returned no results');
  }
  remove = remove || false;
  zoom = zoom || false;
  multi_sites = true;
  if (remove) {
    campsites_group.removeLayer(campsites);
  }
  $.getJSON(query, function (data) {
    //if there is nothing in the returned query, just re-adds all campistes
    if (data.features.length === 0) {
      document.getElementById("popupButton").innerHTML = 'Click To Find Your Campsite!';
      multi_sites = false;
      map.removeControl(editSearch);
      map.addControl(drawControl);
      drawnItems.clearLayers();
      activeBox = false;
      boxBounds = '';
      searched = false;
      searchQuery = campQuery
      return addCampsites(campQuery, true);
    }
    //clears the cards on the right side of page
    while (cardsList.firstChild) {
      cardsList.removeChild(cardsList.firstChild);
    }
    // creates cards based off query
    for (let i = 0; i < data.features.length; i++) {
      if (data.features[i].properties.campsite_address !== null) {
        let tempItem = document.createElement('div');
        tempItem.addEventListener('click', zoomToFeature);
        let child = document.createElement('p');
        tempItem.className = 'siteInfo';
        child.innerHTML = data.features[i].properties.campsite_address;
        tempItem.innerHTML = '<p hidden>' + data.features[i].properties.lat.toString() + '</p> <p hidden> ' + data.features[i].properties.long.toString() + '</p>';
        tempItem.appendChild(child);
        cardsList.appendChild(tempItem);
      }
    }
    campsites = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        if (feature.properties.campsite_address === null) {
          layer.bindPopup('<h2> Address: </h2> <p>  Sorry, no listed address for this site. </p>  <a href="https://www.google.com/maps/search/?api=1&query=' + feature.properties.lat.toString() + ',' + feature.properties.long.toString() + '" target="_blank"> Click for directions! </a>');
        } else {
          layer.bindPopup("<h2> Address: </h2> <p>" + feature.properties.campsite_address + '</p> <a href="https://www.google.com/maps/search/?api=1&query=' + feature.properties.lat.toString() + ',' + feature.properties.long.toString() + '" target="_blank"> Click for directions! </a>');
        }
      },
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
      }
    });
    campsites.addTo(campsites_group);
    if (zoom) {
      //if zoom is passed, skips the fitbounds
    } else {
      map.fitBounds(campsites_group.getBounds()); // zooms to fit data
    }
  });
}
addCampsites(campQuery);

//creates layer with drawn shape 
map.on(L.Draw.Event.CREATED, function (e) {
  var layer = e.layer;
  drawnItems.addLayer(layer);
  map.removeControl(drawControl);
  map.addControl(editSearch);
  searchInBox(e.layer._latlngs[0]);
});

let boxSelectedQuery = "https://jlardy.carto.com/api/v2/sql?format=GeoJSON&q=SELECT * FROM campsite_data WHERE lat BETWEEN ";
let activeBox = false; // true if there is a user drawn box 
let boxBounds = ''; // holder for the bounds of box in SQL format to be appended to regular query if user does popup search

//deletes the drawn objs and re-adds the rectangle draw bar
map.on('draw:deleted', function (e) {
  map.removeControl(editSearch);
  map.addControl(drawControl);
  drawnItems.clearLayers();
  activeBox = false;
  boxBounds = '';
  if (searched) {
    addCampsites(searchQuery, true);
  } else {
    addCampsites(campQuery, true);
  }
})

var finalBoxQuery; //holds the entire query for a user drawn box

//adds sites contained in user drawn box
function searchInBox(box) {
  campsites_group.removeLayer(campsites);
  var minLat = box[0].lat;
  var maxLat = box[2].lat;
  var minLong = box[0].lng;
  var maxLong = box[2].lng;
  activeBox = true;
  boxBounds = " AND lat BETWEEN " + minLat.toString() + " AND " + maxLat.toString() + " AND long BETWEEN " + minLong.toString() + " AND " + maxLong.toString();
  if (searched) {
    // make a query that includes the searchQuery
    finalBoxQuery = searchQuery + boxBounds;
  } else {
    finalBoxQuery = boxSelectedQuery + minLat.toString() + " AND " + maxLat.toString() + " AND long BETWEEN " + minLong.toString() + " AND " + maxLong.toString();
  }
  $.getJSON(finalBoxQuery, function (data) {
    //same error handling as with addCampsites, if there is nothing it returns to the last queried campsites
    if (data.features.length === 0) {
      map.removeControl(editSearch);
      map.addControl(drawControl);
      drawnItems.clearLayers();
      activeBox = false;
      boxBounds = '';
      alert('No Sites in this area.');
      if (searched) {
        return addCampsites(searchQuery, true);
      } else {
        return addCampsites(campQuery, true);
      }
    }
    while (cardsList.firstChild) {
      cardsList.removeChild(cardsList.firstChild);
    }
    for (let i = 0; i < data.features.length; i++) {
      if (data.features[i].properties.campsite_address !== null) {
        let tempItem = document.createElement('div');
        tempItem.addEventListener('click', zoomToFeature);
        let child = document.createElement('p');
        tempItem.className = 'siteInfo';
        child.innerHTML = data.features[i].properties.campsite_address;
        tempItem.innerHTML = '<p hidden>' + data.features[i].properties.lat.toString() + '</p> <p hidden> ' + data.features[i].properties.long.toString() + '</p>';
        tempItem.appendChild(child);
        cardsList.appendChild(tempItem);
      }
    }
    campsites = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        if (feature.properties.campsite_address === null) {
          layer.bindPopup('<h2> Address: </h2> <p>  Sorry, no listed address for this site. </p> <a href="https://www.google.com/maps/search/?api=1&query=' + feature.properties.lat.toString() + ',' + feature.properties.long.toString() + '" target="_blank"> Click for directions! </a>');
        } else {
          layer.bindPopup("<h2> Address: </h2> <p>" + feature.properties.campsite_address + '</p> <a href="https://www.google.com/maps/search/?api=1&query=' + feature.properties.lat.toString() + ',' + feature.properties.long.toString() + '" target="_blank"> Click for directions! </a>');
        }
      },
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
      }
    }).addTo(campsites_group);
  });
};

//adding the layer control to switch to different basemaps
let baselayers = {
  "Grey Map": CartoDB_Positron,
  "Satelite Imagry": sat,
  "Terrain": terrainMap
};

let overlays = {
  "Lakes": lakes_group,
  "Campsites": campsites_group
};

let layerControl = L.control.layers(baselayers, overlays).addTo(map);

//clicking a campsite fills information into a current site on right side of map
let tempText = document.getElementById('site');
let currentCard = document.getElementsByClassName('cardInfo');
let firstIter = true;
let cardKeys = ["campsite_address", "campfire_allowed", "pets_allowed", "max_num_of_people", "max_num_of_vehicles", "site_access"];
let baseText = ["Address: ", "Campfire Allowed: ", "Pets Allowed: ", "Max People: ", "Max Vehicles: ", "Site Access: "];
campsites_group.on('click', function (e) {
  //for when someone clicks off
  map.on('popupclose', function () {
    for (let i = 0; i < currentCard.length; i++) {
      if (i === 0) {
        currentCard[i].innerHTML = '<b> Please click on a campsite to display information </b>';
      } else {
        currentCard[i].innerHTML = '    ';
      }
    }
  });
  if (!firstIter) {
    while (currentCard.firstChild) {
      currentCard.removeChild(currentCard.firstChild);
    }
  }
  firstIter = false;
  for (let i = 0; i < currentCard.length; i++) {
    if (!e.layer.feature.properties[cardKeys[i]]) {
      currentCard[i].innerHTML = '<b>' + baseText[i] + '</b>' + "N/a";
    } else {
      currentCard[i].innerHTML = '<b>' + baseText[i] + '</b>' + e.layer.feature.properties[cardKeys[i]];
    }
  }
});