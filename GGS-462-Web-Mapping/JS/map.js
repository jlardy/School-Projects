//main main obj
var map = L.map("map", {
  zoom: 11
});
let searched = false;

//feature group for drawn objs
var drawnItems = new L.FeatureGroup().addTo(map);
var drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    polygon: false,
    circle: false,
    rectangle: {
      shapeOptions: {
        clickable: false,
        fill: false
      }
    },
    circlemarker: false,
    marker: false
  },
  edit: false
});
map.addControl(drawControl);

// delete tool for drawn shapes
var editSearch = new L.Control.Draw({
  draw: false,
  edit: {
    featureGroup: drawnItems,
    edit: false
  }
});


let key = "pk.eyJ1IjoiamVsYXJkZSIsImEiOiJjand0bXJlOTAwNmZyNDRwZWRqcHEyYWpkIn0.Q37dvPwAVcEKGpNtOJ5Hwg";

// Basemaps
var CartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 24
}).addTo(map);

var terrainMap = new L.StamenTileLayer("terrain");

var sat = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 24,
  id: 'mapbox.satellite',
  accessToken: key
});



//styles
var geojsonMarkerOptions = {
  radius: 8,
  fillColor: "#6666ff",
  color: "#000",
  weight: 1,
  opacity: 1,
  fillOpacity: 0.5
};