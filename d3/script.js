
function csvToArr(stringVal, splitter) {
    const [keys, ...rest] = stringVal
        .trim()
        .split("\n")
        .map((item) => item.split(splitter));
    
        const formedArr = rest.map((item) => {
        const object = {};
        keys.forEach((key, index) => (object[key] = item.at(index)));
        return object;
        });
    return formedArr;
}

function showInfo() {
    var dropdown = document.getElementById("dropdown");
    var year = dropdown.value;
    var infoDiv = document.getElementById("yearInfo");

    infoDiv.innerHTML = "";

    if (year == "2020"){
        infoDiv.innerHTML = "2020";
        console.log(csvToArr('data.csv', ','))
    } else if (year == "2021"){
        infoDiv.innerHTML = "2021";
    } else if (year == "2022"){
        infoDiv.innerHTML = "2022";
    } else if (year == "2023"){
        infoDiv.innerHTML = "2023";
    } else if (year == "2024"){
        infoDiv.innerHTML = "2024";
    } else {
        infoDiv.innerHTML = "All Years";
    }

}




