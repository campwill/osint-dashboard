String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
function createAndAppendElements(data, container, dictionary, ignoredItems) {
    for (var key in data) {
        if (!ignoredItems.includes(key)) {
            var item = document.createElement("div");
            var value = key in dictionary ? dictionary[key] + ": " + data[key] : key.toProperCase() + ": " + data[key];
            item.innerText = value;
            container.appendChild(item);
            var hr = document.createElement("hr");
            container.appendChild(hr);
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var largeJsonScript = document.getElementById('large-json-data');
    var largeJsonData = JSON.parse(largeJsonScript.getAttribute('data-large-json'));

    var cookiesInfoDiv = document.querySelector(".cookies-info");
    createAndAppendElements(largeJsonData["cookies"], cookiesInfoDiv, {}, []);

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
    createAndAppendElements(largeJsonData['ip_info'],IPInfoDiv,IPDict,irrelevant_items);

    var headersInfoDiv = document.querySelector(".header-info");
    irrelevant_items = ["perf", "expiry", "set-cookie"];
    let HeaderDict = {
        "pragma" : "Pragma (Catching) Info",
        "server" : "Web Server Info"
    }
    createAndAppendElements(largeJsonData["headers"],headersInfoDiv,HeaderDict,irrelevant_items);

    var DNSInfoDiv = document.querySelector(".DNS-info");
    irrelevant_items = [];
    let DNSDict = {
        "A" : "'A' (address) Record",
        "NS" : "'NS' (nameserver) Record",
        "SOA" : "'SOA' (start of authority) Record",
        "MX" : "'MX' (mail exchange) Record"
    }
    createAndAppendElements(largeJsonData["dns_records"],DNSInfoDiv,DNSDict,[])
});
