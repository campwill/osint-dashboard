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
var toolsConfig = [
    {
        containerSelector: ".cookies-info",
        dataKey: "cookies",
        dictionary: {},
        ignoredItems: []
    },
    {
        containerSelector: ".ip-information",
        dataKey: "ip_info",
        dictionary: {
            "ip" : "IP",
            "anycast" : "Anycast network architecture",
            "loc" : "Coordinates",
            "org" : "Organization",
            "postal" : "ZIP Code",
            "country_name" : "Country"
        },
        ignoredItems: ["isEU", "country_flag_url", "country", "country_flag", "country_currency", "continent", "latitude", "longitude"]
    },
    {
        containerSelector: ".header-info",
        dataKey: "headers",
        dictionary: {
            "pragma" : "Pragma (Catching) Info",
            "server" : "Web Server Info"
        },
        ignoredItems:["perf", "expiry", "set-cookie"]
    },
    {
        containerSelector:".DNS-info",
        dataKey: "dns_records",
        dictionary: {
            "A" : "'A' (address) Record",
            "NS" : "'NS' (nameserver) Record",
            "SOA" : "'SOA' (start of authority) Record",
            "MX" : "'MX' (mail exchange) Record"
        },
        ignoredItems: []
    },
    {
        containerSelector:".SSL-info",
        dataKey:"ssl_info",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".redirects-info",
        dataKey: "redirects",
        dictionary:{},
        ignoredItems:[]
    }

];
document.addEventListener('DOMContentLoaded', function() {
    var largeJsonScript = document.getElementById('large-json-data');
    var largeJsonData = JSON.parse(largeJsonScript.getAttribute('data-large-json'));

    toolsConfig.forEach(function (config) {
        var container = document.querySelector(config.containerSelector);
        createAndAppendElements(largeJsonData[config.dataKey], container, config.dictionary, config.ignoredItems);
    });
});
