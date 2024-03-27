async function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: '946a9c10600de2ba'
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    for (let item of posts) {
        const title = item.fields.title;
        const description = item.fields.description;
        const postID = item.pk; // Get the post ID
        const position = { lat: item.fields.geoCode.geometry.location.lat, lng: item.fields.geoCode.geometry.location.lng };
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

        const marker = new AdvancedMarkerElement({
            position,
            map,
            title: title,
        });
        const infowindow = new google.maps.InfoWindow({
            content: `
                <h3>${title}</h3>
                <p>${description}</p>
                <a href="#" onclick="openSlideshow(${postID})">See More</a> <!-- Call openSlideshow function -->
            `
        });
        
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}

// Function to open the slideshow popup
function openSlideshow(postID) {
    window.location.href = `/slideshow/${postID}/`;
}
