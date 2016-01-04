$("#menu-text").keyup(parseMenu);
$("#menu-type").change(menuTypeChange);
$("#save-button").click(submitMenu);
$(".form-control").change(parseMenu);

var outer = "";
var menus = [];
var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];

function menuTypeChange() {
    if($("#menu-type").val() == 'D') {
        $("#single-meal-fields").show();
    } else {
        $("#single-meal-fields").hide();
    }
    clearParsedMenu();
}

function clearParsedMenu() {
    var html = '<div class="well">Please enter some menu text into the field to the left.</div>';
    jQuery("#parsed-menu").html(html);
}


function parseMenu() {
    if($("#menu-type").val() == 'L') {
        parseAndrosMenu();
    } else {
        parseMealMenu();
    }
}

function parseMealMenu() {
    menus = [];
    var ds = $("#menu-date").val().split('-');
    var date = new Date(ds[0], ds[1]-1, ds[2]);
    var menu = {
        date: date,
        cuisine: $("#menu-cuisine").val().trim(),
        items: [],
        vendor: $("#menu-vendor").val().trim(),
        mealType: $("#meal-type").val()
    };
    var menuText = $("#menu-text").val().trim();
    var lines = menuText.split('\n');
    for(var i=0;i<lines.length;i++) {
        var line = lines[i];
        menu.items.push(line);
    }
    if (menu.date==null || menu.cuisine == "" || menu.items.length == 0 || menu.vendor == "" || menu.mealType == "") {
        clearParsedMenu();
        $("#save-button").prop('disabled', true);
        return;
    }
    $("#save-button").prop('disabled', false);
    menus.push(menu);
    drawMenu();
}


function parseAndrosMenu() {
    var menuText = $("#menu-text").val().trim();
    var re = /^((?:Mon|Tues|Wednes|Thurs|Fri)day),\s(\w+)\s([0-9]+)\n(\w+)/mg;
    var subst = '|$1|$2|$3|$4';
    var result = menuText.replace(re, subst);
    outer = result
    var lines = result.split('\n');
    var menu = null;
    menus = [];
    for(var i=0;i<lines.length;i++) {
        var line = lines[i];
        if(line.indexOf('|')==0) {
            console.log(line);
            var header = line.split('|');
            //console.log(header);
            var weekday = header[1];
            var month = monthNames.indexOf(header[2]);
            var day = header[3];
            var date = new Date(2016, month, day, 12, 0, 0);
            var cuisine = header[4];
            var menu = {
                date:date,
                cuisine:cuisine,
                items:[],
                vendor: 'Andros',
                mealType: 'L'
            };
            menus.push(menu);
        } else {
            if(menu!=null) {
                menu.items.push(line);
            }
        }
    }
    if(menu!=null) {
        $("#save-button").prop('disabled', false);
        drawMenu();
    } else {
        $("#save-button").prop('disabled', true);
    }
}

function drawMenu() {
    var html = "";
    for(var i=0;i<menus.length;i++) {
        var menu = menus[i];
        var mealType = menu.mealType == 'L' ? 'Lunch' : 'Dinner';
        html += '<div class="meal-block">' +
            '<h2>' + dateToString(menu.date) + ' - ' + mealType + '</h2>' +
            '<h3>' + menu.vendor + '</h3>' +
            '<h4>' + menu.cuisine + '</h4>' +
            '<ul>';
        for(var j=0;j<menu.items.length;j++) {
            html += '<li>' + menu.items[j] + '</li>';
        }
        html += '</ul>' +
            '</div>';
    }
    jQuery("#parsed-menu").html(html);
}

function dateToString(date) {
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();

    return monthNames[monthIndex] + ' ' + day + ', ' + year;
}

function submitMenu() {
    var payload = JSON.stringify(menus);
    var url = '/submit/';
    jQuery.post(url, payload, function(result) {
        var html = result + '<a href="/parse" class="btn btn-primary">Enter Another</a>';
        $("#content").html(html);
    });
    return false;
};
