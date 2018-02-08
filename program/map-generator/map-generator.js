//Notes for the code necessary for the generator as well as necessary features
//We need it to output valid config files given in the example file in the maps file in assets
//For the "map = " portion, Arrays nested in arrays will be necessary
var mapArray,
    currentX = 0,
    currentY = 0,
    oldMapValue = ".";
const cursor = "■"

var property = {
    propertyName: "",
    propertyValue: "";
};

var tile = {
    tilename: "",
    properties: []
};

var tileMatrix = [];

function loadKeyHandler() {
    document.getElementById("mapOutput").addEventListener("keydown", keyHandler, false);
}

function keyHandler(e) {
    processCurrentKey(e.keyCode);
}

function processCurrentKey(key) {

    switch (key) {
        case 40: //Down
            if (currentY >= mapArray.length - 1) {
                currentY = mapArray.length - 1;
                break;
            }
            console.log("down");
            setSpotOnMap(currentX, currentY, oldMapValue);
            currentY++;
            oldMapValue = getValueOfMap(currentX, currentY);
            setSpotOnMap(currentX, currentY, cursor);
            break;
        case 38: //Up
            if (currentY <= 0) {
                currentY = 0;
                break;
            }
            console.log("up");
            setSpotOnMap(currentX, currentY, oldMapValue);
            currentY--;
            oldMapValue = getValueOfMap(currentX, currentY);
            setSpotOnMap(currentX, currentY, cursor);
            break;
        case 37: //Left
            if (currentX <= 0) {
                currentX = 0;
                break;
            }
            console.log("left");
            setSpotOnMap(currentX, currentY, oldMapValue);
            currentX--;
            oldMapValue = getValueOfMap(currentX, currentY);
            setSpotOnMap(currentX, currentY, cursor);
            break;
        case 39: //Right
            if (currentX >= mapArray[0].length - 1) {
                currentX = mapArray[0].length - 1;
                break;
            }
            console.log("right");
            setSpotOnMap(currentX, currentY, oldMapValue);
            currentX++;
            oldMapValue = getValueOfMap(currentX, currentY);
            setSpotOnMap(currentX, currentY, cursor);
            break;
        default:
            console.log("key");
            setSpotOnMap(currentX, currentY, String.fromCharCode(key));
            oldMapValue = String.fromCharCode(key);
            break;
    }
    drawMap();
    tileLocation();
}

function setSpotOnMap(x, y, char) {
    mapArray[y][x] = char;
}

function getValueOfMap(x, y) {
    return mapArray[y][x];
}


function drawMap() {
    var out = document.getElementById("mapOutput");
    var line;
    line = "map = ";
    for (let i = 0; i < mapArray.length; i++) {
        for (let j = 0; j < mapArray[i].length; j++) {
            line = line + getValueOfMap(j, i);
        }
        line = line + "<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    }
    out.innerHTML = line;

}

function defineMapSize() {
    var mapSizeX = parseInt(document.getElementById("mapSizeX").value),
        mapSizeY = parseInt(document.getElementById("mapSizeY").value);
    mapArray = null;
    mapArray = [mapSizeY];
    for (let i = 0; i < mapSizeY; i++) {
        mapArray[i] = new Array(mapSizeX);
    }

    for (let i = 0; i < mapArray.length; i++) {
        for (let j = 0; j < mapArray[i].length; j++) {
            setSpotOnMap(j, i, ".");
        }
    }
}

function addTile() {
    //NOTE: In the tile matrix, index 0 of the 2nd dimension is the tile name

    var tileName = document.getElementById("tileName").value.trim(),
        property = document.getElementById("property").value.trim(),
        propertyValue = document.getElementById("propertyValue").value.trim();


}

function outputTileProperties() {
    var tileOutput = ""
    
    document.getElementById("tilePropertiesOutput").innerHTML = tileOutput;
}


     //Just to show the x, y coordinate of where you are in the array
function tileLocation() {
    var z = document.getElementById("valueOutput").value;
    document.getElementById("valueOutput").innerHTML = ("tilex = " + (currentX + 1) + "<br>" + "tiley = " + (currentY + 1));
}
