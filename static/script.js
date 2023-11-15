document.addEventListener('DOMContentLoaded', function() {
    var largeJsonScript = document.getElementById('large-json-data');
    var largeJsonData = JSON.parse(largeJsonScript.getAttribute('data-large-json'));

    var cookiesData = largeJsonData["cookies"];
    var cookiesInfoDiv = document.querySelector(".cookies-info");
    for (var key in cookiesData) {
        var item = document.createElement("div");
        item.innerText = key + ": " + cookiesData[key];
        cookiesInfoDiv.appendChild(item);
    }

    var IPData = largeJsonData["ip_info"];
    console.log(IPData);
    var IPInfoDiv = document.querySelector(".ip-information");
    irrelevant_items = ["isEU", "country_flag_url", "country", "country_flag", "country_currency", "continent", "latitude", "longitude" ];

    let IPDict = {
        "ip" : "IP",
        "anycast" : "Anycast network architecture",
        "loc" : "Coordinates",
        "org" : "Organization",
        "postal" : "ZIP Code",
        "country_name" : "Country"
    }

    for(var key in IPData){

        if( !irrelevant_items.includes(key)){
            var item = document.createElement("div");
            item.innerText = IPDict[key].toUpperCase()+ ": " + IPData[key];
            IPInfoDiv.appendChild(item);
        }
    }
    var HeaderData = largeJsonData["headers"];
    var headersInfoDiv = document.querySelector(".header-info");
    irrelevant_items = ["perf", "expiry", "set-cookie"];

    let HeaderDict = {
        "pragma" : "Pragma (Catching) Info",
        "server" : "Web Server Info"
    }

    for (var key in HeaderData) {

        if( !irrelevant_items.includes(key)){
            var item = document.createElement("div");
            item.innerText = HeaderDict[key].toUpperCase() + ": " + HeaderData[key];
            headersInfoDiv.appendChild(item);
        }
    }
    var DNSData = largeJsonData["dns_records"];
    var DNSInfoDiv = document.querySelector(".DNS-info");
    irrelevant_items = [];

    let DNSDict = {
        "A" : "'A' (address) Record",
        "NS" : "'NS' (nameserver) Record",
        "SOA" : "'SOA' (start of authority) Record",
        "MX" : "'MX' (mail exchange) Record"
    }

    for (var key in DNSData) {

        if( !irrelevant_items.includes(key)){
            var item = document.createElement("div");
            item.innerText = DNSDict[key].toUpperCase() + ": " + DNSData[key];
            DNSInfoDiv.appendChild(item);
        }
    }

});
