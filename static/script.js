String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
function createAndAppendElements(data, container, dictionary, ignoredItems) {
    for (var key in data) {
        console.log(key)
        if (key == 'screenshot'){
            var hr = document.createElement("hr");
            container.appendChild(hr);
            var item = document.createElement("div");
            value = "<img style=\"height: 100%; width:100%;\" src=\"data:image/png;base64," + data[key] + "\"\\>"

            item.innerHTML = value;
            container.appendChild(item)
        }
        else if (!ignoredItems.includes(key)) {
            var hr = document.createElement("hr");
            container.appendChild(hr);
            var item = document.createElement("div");

            var value;
            if (Array.isArray(data[key])) {
                value = key.toProperCase() + ": ";
                data[key].forEach(function (element) {
                    value += "<br>"+element  ;
                });
            } else {
                value = key in dictionary ? dictionary[key] + ": " + data[key] : key.toProperCase() + ": " + data[key];
            }

            item.innerHTML = value;
            container.appendChild(item);

            if(key === "country_name")
            {
                var hr = document.createElement("hr");
                container.appendChild(hr);

                var ipmap = document.createElement("div");
                ipmap.setAttribute("id", "map")
                ipmap.setAttribute("style", "height:40vh ;width:100%;")
        
                ipmap.innerHTML = value;
                container.appendChild(ipmap)
        
                var map = L.map('map').setView([data["latitude"], data["longitude"]], 10);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                var marker = L.marker([data["latitude"], data["longitude"]]).addTo(map);
            }
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
            "org" : "Organization",
            "postal" : "ZIP Code",
            "country_name" : "Country"
        },
        ignoredItems: ["isEU", "country_flag_url", "country", "country_flag", "country_currency", "continent", "loc"]
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
        dictionary:{"Redirects": "Redirected From"},
        ignoredItems:[]
    },
    {
        containerSelector:".sitemap-info",
        dataKey:"sitemap",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".ports-info",
        dataKey:"port_info",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".whois-info",
        dataKey:"whois_info",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".screenshot-info",
        dataKey:"screenshot",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".links-info",
        dataKey:"link_info",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".emails-info",
        dataKey:"email_info",
        dictionary:{},
        ignoredItems:[]
    },
    {
        containerSelector:".phone-info",
        dataKey:"phone_info",
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

