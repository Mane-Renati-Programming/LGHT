//Notes for the code necessary for the generator as well as necessary features
//We need it to output valid config files given in the example file in the maps file in assets
//For the "map = " portion, Arrays nested in arrays will be necessary
var mapArray,
    currentX = 0,
    currentY = 0,
    oldMapValue = ".";
const cursor = "■"

function Property() {
    this.propertyName = "";
    this.propertyValue = "";
}

function Tile() {
    this.tileName = "";
    this.properties = [];
}

var tileMatrix = [];

function loadKeyHandler() {
    document.getElementById("mapOutput").addEventListener("keydown", keyHandler, false);
}

function keyHandler(e) {
    processCurrentKey(e.key);
}

function processCurrentKey(key) {

    switch (key) {
        case "ArrowDown": //Down
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
        case "ArrowUp": //Up
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
        case "ArrowLeft": //Left
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
        case "ArrowRight": //Right
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
        case "Delete":
        case " ":
            key = ".";
        default:
            console.log("key");
            setSpotOnMap(currentX, currentY, key[0]);
            oldMapValue = key[0];
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
    var line = "";
    for (let i = 0; i < mapArray.length; i++) {
        for (let j = 0; j < mapArray[i].length; j++) {
            line = line + getValueOfMap(j, i);
        }
        line = line + "<br>";
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

    var tileName = document.getElementById("tileName").value.trim(),
        property = document.getElementById("property").value.trim(),
        propertyValue = document.getElementById("propertyValue").value.trim();

        //We check for an empty array
        if (tileMatrix.length == 0) {
            console.log("init tileMatrix");
            //It's empty, so we need to start it off
            tileMatrix.push(new Tile());
            tileMatrix[0].tileName = tileName;
            tileMatrix[0].properties.push(new Property());
            tileMatrix[0].properties[0].propertyName = property;
            tileMatrix[0].properties[0].propertyValue = propertyValue;
            outputTileProperties();
            return;
        }

        //It's not empty, so we go through the thing checking for the tile name given
        for (let i = 0; i < tileMatrix.length; i++) {
            if (tileMatrix[i].tileName == tileName) {
                //The tile name is already there, so we just search through its properties
                for (let j = 0; j < tileMatrix[i].properties.length; j++) {
                    if (tileMatrix[i].properties[j].propertyName == property) {
                        //We found that property, so we just update that property
                        console.log("Change property");
                        tileMatrix[i].properties[j].propertyValue = propertyValue;
                        outputTileProperties();
                        return;
                    }
                }
                console.log("add property existing");
                //We never found that property, so we add that property
                tileMatrix[i].properties.push(new Property());
                tileMatrix[i].properties[tileMatrix[i].properties.length - 1].propertyName = property;
                tileMatrix[i].properties[tileMatrix[i].properties.length - 1].propertyValue = propertyValue;
                outputTileProperties();
                return;
            }
        }
        console.log("Add tile");
        //We never found that tile name, so we add it, plus its property
        tileMatrix.push(new Tile());
        tileMatrix[tileMatrix.length - 1].tileName = tileName;
        tileMatrix[tileMatrix.length - 1].properties.push(new Property());
        tileMatrix[tileMatrix.length - 1].properties[0].propertyName = property;
        tileMatrix[tileMatrix.length - 1].properties[0].propertyValue = propertyValue;
        outputTileProperties();
}

function outputTileProperties() {
    var tileOutput = ""
    for (let i = 0; i < tileMatrix.length; i++) {
        tileOutput = tileOutput + "[" + tileMatrix[i].tileName + "]<br>";
        for (let j = 0; j < tileMatrix[i].properties.length; j++) {
            tileOutput = tileOutput + tileMatrix[i].properties[j].propertyName + " = " + tileMatrix[i].properties[j].propertyValue + "<br>";
        }
    }
    document.getElementById("tilePropertiesOutput").innerHTML = tileOutput;
}


     //Just to show the x, y coordinate of where you are in the array
function tileLocation() {
    var z = document.getElementById("valueOutput").value;
    document.getElementById("valueOutput").innerHTML = ("tilex = " + (currentX + 1) + "<br>" + "tiley = " + (currentY + 1));
}
