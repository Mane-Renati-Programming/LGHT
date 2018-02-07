//Notes for the code necessary for the generator as well as necessary features
        //We need it to output valid config files given in the example file in the maps file in assets
        //For the "map = " portion, Arrays nested in arrays will be necessary
        var mapArray,
            currentX = 0,
            currentY = 0,
            oldMapValue = ".";
        const cursor = "■"

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


            //Init the matrix
            if (tileMatrix.length == 0) {
                tileMatrix.push(new Array(3));
                tileMatrix[0][0] = tileName;
                tileMatrix[0][1] = new Array(2);
                tileMatrix[0][1][0] = property;
                tileMatrix[0][1][1] = propertyValue;
                outputTileProperties();
                return;
            }

            for (let i = 0; i < tileMatrix.length - 1; i++) {
                //Iterate through every single matricee checking for the tile given
                if (tileMatrix[i][0] == tileName) {
                    //Since it was already defined, we can just check if that property already exists, and if so, we can just change it.
                    for (let j = 1; j < tileMatrix[i].length - 1; j++) {
                        console.log(j);
                        if (tileMatrix[i][j][0] == property) {
                            //It already exists, so we can just update that value
                            tileMatrix[i][j][1] = propertyValue;
                            outputTileProperties();
                            //We return since we're done and have updated the value
                            return;
                        }
                    }
                    //Since we didn't find it, we add that property to the tile
                    tileMatrix[i].push(new Array(2));
                    tileMatrix[i][tileMatrix[i].length - 1][0] = property;
                    tileMatrix[i][tileMatrix[i].length - 1][1] = propertyValue;
                    outputTileProperties();
                    return;
                }
            }
            //We never found the tile, so we add the tile and add that property
            tileMatrix.push(new Array(3));
            tileMatrix[tileMatrix.length - 1][0] = tileName;
            tileMatrix[tileMatrix.length - 1][1] = new Array(2);
            tileMatrix[tileMatrix.length - 1][1][0] = property;
            tileMatrix[tileMatrix.length - 1][1][1] = propertyValue;
            outputTileProperties();

        }

        function outputTileProperties() {
            var tileOutput = ""
            for (let i = 0; i < tileMatrix.length - 1; i++) {
                tileOutput = tileOutput + "<br>[" + tileMatrix[i][0] + "]";
                for (let j = 1; j < tileMatrix[i].length - 1; j++) {
                    tileOutput = tileOutput + "<br>" + tileMatrix[i][j][0] + " = " + tileMatrix[i][j][1];
                }
            }
            document.getElementById("tilePropertiesOutput").innerHTML = tileOutput;
        }
