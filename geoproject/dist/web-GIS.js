// full sreeen function
var mapId = document.getElementById('map');


function fullScreenview() {
    mapId.requestFullscreen();
}


// when the mouse is over the map - when the map fires the event mousemove
map.on('mousemove', function(e) {

    // this is a nice way to chek if the info I want is got correctly
    console.log(e);
    // console.log(e.latlng.lat);
    // console.log(e.latlng.lng);

    // replace the content of the element having class coordinate with the html
    $('.coordinate').html(`Lat: ${e.latlng.lat} Long: ${e.latlng.lng}`);
});


// print map
$('.print-map').click(function(){
    window.print();
});


// uses this library got from remote
// ./lib/leaflet.browser.print.min.js
//  to load a print wdget on the map
L.control.browserPrint().addTo(map);


// this loads on the map a widget to measure distances . leaflet-measure
L.control.measure({
    primaryLengthUnit: 'meters',
    primaryAreaUnit:'sqmeters',
    secondaryLengthUnit: 'kilometers',
}).addTo(map);


// leaflet search add
L.Control.geocoder().addTo(map)


// leaflet zoom
$('.zoom-to-layer').click(function(){
    map.setView([44.8683931,9.2651729], 14)
})
