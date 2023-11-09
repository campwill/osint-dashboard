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
    irrelevant_items = ["isEU","country_currency"];
    for(var key in IPData){

        if( !irrelevant_items.includes(key)){
            var item = document.createElement("div");
            if(key == "ip"){
                item.innerText = "IP: " + IPData[key];
            }else{
            item.innerText = key+ ": " + IPData[key];
            }
            IPInfoDiv.appendChild(item);

        }
    }
    var HeaderData = largeJsonData["headers"];
    var headersInfoDiv = document.querySelector(".header-info");
    for (var key in HeaderData) {
        if(key !="Set-Cookie"){

            var item = document.createElement("div");
            item.innerText = key + ": " + HeaderData[key];
            headersInfoDiv.appendChild(item);
        }   
    }
    var DNSData = largeJsonData["dns_records"];
    var DNSInfoDiv = document.querySelector(".DNS-info");
    for (var key in DNSData) {
        var item = document.createElement("div");
        item.innerText = key + ": " + DNSData[key];
        DNSInfoDiv.appendChild(item);
    }
    

});
