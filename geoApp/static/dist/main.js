
// initializig the class map
// var map = L.map('map', {
//     measureControl: true, // this is necessary to allow the measure lib to work
// }    ).setView([44.8683931,9.2651729], 15);
// otherwise,
var map = L.map('map', {dragging: true}).setView([44.8683931,9.2651729], 14);

// would be enough

// zoomcontrol is already integrated by leaflet ... right?
map.zoomControl.setPosition('topright');

    // adding osm layer
// L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// now saving the tile into a variable and adding it to the map
var osm_basemap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// adding another basemap - from https://leaflet-extras.github.io/leaflet-providers/preview/
var watercolor_basemap = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 1,
    maxZoom: 16,
    ext: 'jpg'
});

// var Jawg_Light = L.tileLayer('https://{s}.tile.jawg.io/jawg-light/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
//     attribution: '<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
//     minZoom: 0,
//     maxZoom: 22,
//     subdomains: 'abcd',
//     accessToken: '<your accessToken>' // this requires a premium account?
// });

var tonerlite_basemap = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20,
    ext: 'png'
});

// main marker
//  define its style - https://stackoverflow.com/questions/23567203/leaflet-changing-marker-color
var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
    });

L.marker([44.8683931,9.2651729], {icon: greenIcon}).addTo(map)
    .bindPopup('Zavattarello')  // label on my pointer
    .openPopup();

// add map scale
L.control.scale().addTo(map);

// these are moved into webgis.js

// // full sreeen function -  
// var mapId = document.getElementById('map');

// function fullScreenview() {
//     mapId.requestFullscreen();
// }

// display the coordinates of the point pf hte map where the mouse is
// i need jquery for this

// // when the mouse is over the map - when the map fires the event mousemove
// map.on('mousemove', function(e) {


//     // this is a nice way to chek if the info I want is got correctly
//     console.log(e);
//     // console.log(e.latlng.lat);
//     // console.log(e.latlng.lng);

//     // replace the content of the element having class coordinate with the html
//     $('.coordinate').html(`Lat: ${e.latlng.lat} Long: ${e.latlng.lng}`);
// });

// // print map
// $('.print-map').click(function(){
//     window.print();
// });

// // uses this library got from remote
// // ./lib/leaflet.browser.print.min.js
// //  to load a print wdget on the map
// L.control.browserPrint().addTo(map);

// // this loads on the map a widget to measure distances . leaflet-measure
// L.control.measure({
//     primaryLengthUnit: 'meters',
//     primaryAreaUnit:'sqmeters',
//     secondaryLengthUnit: 'kilometers',
// }).addTo(map);  

// end of moving to webis.js


// load geojson data on the map
// L.geoJSON(map_data_1).addTo(map);
// deleted to be replaced with markercluster

// now with marker cluster
var marker = L.markerClusterGroup(); // initialize var marker from class markerclustergroup

// var map_data_v1 = L.geoJSON(map_data_1);

var map_data_v1 = L.geoJSON(map_data_1, {
    onEachFeature: function(feature, layer) {
        // layer.bindPopup('test label')
        layer.bindPopup(feature.properties.name)
    }
});

map_data_v1.addTo(marker);

// marker.addTo(map); // disabled in lesson 10 to add more code further below

//  moved to main.js
// // leaflet search add
// L.Control.geocoder().addTo(map)



// leaflet layer contorl
var baseMaps = {
    'OSM': osm_basemap,
    'Water Color Map': watercolor_basemap,
    'Toner Light Map':tonerlite_basemap
}

// the teacher calls it overlayMaps
var geodataLayers = {
    'GeoJSON Markers': marker
}

// L.control.layers(baseMaps, geodataLayers, ).addTo(map)

// # this adds the markers to the map
// L.control.layers(baseMaps, geodataLayers, {collapsed: false, position: 'topleft'}).addTo(map)

// activate the marekrs by default y simply - then you can uncklick them from menu
marker.addTo(map);


// moved to main.js
// // leaflet zoom
// $('.zoom-to-layer').click(function(){
//     map.setView([44.8683931,9.2651729], 14)
// })


// make the map draggable only when space (key32) is hold down
// map.dragging.disable();
// // Keydown and keyup event
// document.body.onkeydown = function(e){
//     if(e.keyCode == 32){
//         map.dragging.enable();
//     }
// }
// document.body.onkeyup = function(e){
//     if(e.keyCode == 32){
//         map.dragging.disable();
//     }
// }



