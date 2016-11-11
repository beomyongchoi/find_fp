/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

function getLocation() {
    Modernizr.geolocation ? navigator.geolocation.getCurrentPosition(currentLocation, handle_error, {
        timeout: 1e4
    }) : ($wait.fadeOut(), $locationBar.fadeIn())
}

function handle_error(e) {
    $locationBar.css("opacity", 1), showError("can't find your fucking location"), 0 == e.code, 1 == e.code, 2 == e.code, 3 == e.code
}

function currentLocation(e) {
    $wait.fadeIn(), $locationBar.fadeOut();
    var o = e.coords.latitude,
        t = e.coords.longitude;
    currentlatlng = new google.maps.LatLng(o, t), getPlaces(currentlatlng)
}

function getPlaces(e) {
    userLoc = e, homeMarker = new google.maps.Marker({
        map: map,
        animation: google.maps.Animation.DROP,
        position: e,
        icon: homeIcon
    });
    var o = {
        location: e,
        radius: 1e3,
        keyword: "restaurant"
    };
    service.search(o, storeRequestBar)
}

function storeRequestBar(e) {
    barResultsStore = e;
    var o = {
        location: currentlatlng,
        radius: 1e3,
        keyword: "restaurant"
    };
    service.search(o, storeRequestPub)
}

function storeRequestPub(e) {
    for (pubResultsStore = e, totalResults = barResultsStore.concat(pubResultsStore), resultsStore = removeDupes(totalResults, "id"), resultsStore = resultsStore.sort(function() {
            return Math.random() - .5
        }), i = 0; i < resultsStore.length; i++);
    0 == resultsStore && showError("can't find shit there. try somewhere else"), chooseBar(resultsStore)
}

function chooseBar(e) {
    barRef = {
        reference: e[shitCounter].reference
    }, service.getDetails(barRef, showBar)
}

function showBar(e, o) {
    if (o == google.maps.places.PlacesServiceStatus.OK) {
        for (i in markersArray) markersArray[i].setMap(null);
        drinkMarker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            position: e.geometry.location,
            icon: drinkIcon
        }), markersArray.push(drinkMarker), placeName = e.name, calcRoute(userLoc, e.geometry.location), directionsDisplay.setMap(null), directionsDisplay.suppressMarkers = !0, directionsDisplay.polylineOptions = {
            strokeColor: "#ff8400",
            strokeOpacity: .8,
            strokeWeight: 5
        }, directionsDisplay.setMap(map), placeSite = e.website ? e.website : e.url, placeAddress = e.formatted_address, $(".recommendation__destination").html("Why don't you fucking go to <br/><a href='" + placeSite + "' target='_blank' title='VISIT THE FUCKING WEBSITE'>" + placeName + "</a>"), $(".map__address").html(placeAddress), $(".grid__row--links,.grid__row--actions,.adsense,.recommendation,.map__address,.recommendation__destination").fadeIn(function() {
            $wait.fadeOut()
        })
    }
}

function calcRoute(e, o) {
    var t = {
        origin: e,
        destination: o,
        travelMode: google.maps.TravelMode.WALKING
    };
    directionsService.route(t, function(e, o) {
        o == google.maps.DirectionsStatus.OK && directionsDisplay.setDirections(e)
    })
}

function codeAddress() {
    $wait.fadeIn(function() {
        $locationBar.fadeOut();
        var e = document.getElementById("locationsearch").value;
        geocoder.geocode({
            address: e
        }, function(e, o) {
            o == google.maps.GeocoderStatus.OK ? (currentlatlng = e[0].geometry.location, getPlaces(currentlatlng)) : showError("can't find your fucking location. try again")
        })
    })
}

function showError(e) {
    $wait.fadeOut(), $locationBar.fadeIn(), $(".locator__message").text(e).fadeIn()
}

function removeDupes(e, o) {
    var t = [],
        r = {};
    for (var a in e) r[e[a][o]] = e[a];
    for (a in r) t.push(r[a]);
    return t
}
var resultref, marker, markersArray = [],
    shitCounter = 0,
    iteration = 0,
    drinkIcon = "img/food.png",
    homeIcon = "img/home.png",
    resultsStore, totalResults = [],
    pubResultsStore, barResultsStore, userLoc, currentlatlng;
$wait = $(".loader"), $locationBar = $(".locator"), $mapCanvas = $(".map__canvas");
var lowSat = [{
        featureType: "all",
        stylers: [{
            saturation: -100
        }]
    }],
    myOptions = {
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: lowSat,
        mapTypeControl: !1,
        panControl: !1,
        zoomControl: !0,
        mapTypeControl: !1,
        scaleControl: !1,
        streetViewControl: !1,
        overviewMapControl: !1
    };
map = new google.maps.Map(document.getElementById("googlemap"), myOptions), geocoder = new google.maps.Geocoder;
var service = new google.maps.places.PlacesService(map);
$(document).ready(function() {
    var e = window.location.href,
        o = e.split("?");
    "wherethefuck" == o[1] ? $locationBar.css("opacity", 1) : getLocation()
});
var directionsDisplay = new google.maps.DirectionsRenderer({
        suppressMarkers: !0
    }),
    directionsService = new google.maps.DirectionsService;
$(".locator").on("submit", function(e) {
    codeAddress(), e.preventDefault()
}), $(".actions__shit").click(function() {
    return shitCounter < resultsStore.length - 1 ? shitCounter++ : shitCounter = 0, chooseBar(resultsStore), window.scroll(0, 0), !1
});
var autoOptions = {
        types: ["geocode"]
    },
    autoInput = document.getElementById("locationsearch");
autocomplete = new google.maps.places.Autocomplete(autoInput, autoOptions);
