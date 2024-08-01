
//Shapefile wms
{% for s in shp %}
var {{ s.name }} = L.tileLayer.wms('http://localhost:8080/geoserver/wms', {
    layers: '{{s.name}}',
    transparent: true,
    format: 'image/png',
})
overlayMaps['{{ s.name }}'] = {{ s.name }}

{% endfor %}

//Tiff wms
{% for t in tiff %}
var {{ t.name }} = L.tileLayer.wms('http://localhost:8080/geoserver/wms', {
    layers: '{{t.name}}',
    transparent: true,
    format: 'image/png',
})

overlayMaps['{{ t.name }}'] = {{ t.name }}

{% endfor %}

