add = document.getElementById("add");
add.addEventListener("click", () => {
    title = document.getElementById("title").value;
    date = document.getElementById("date").value;
    time = document.getElementById("time").value;
    des = document.getElementById("description").value;
    date= date+" | "+time;
    
    if (localStorage.getItem("itemsjson") == null) {
        itemjsonarray = [];
        itemjsonarray.push([title, date, des]);
        localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));

    } else {
        itemjsonarraystr = localStorage.getItem("itemsjson");
        itemjsonarray = JSON.parse(itemjsonarraystr);
        itemjsonarray.push([title, date, des]);
        localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));

    }
    console.log("item added");
    // update the table.
    let tablebody = document.getElementById("tablebody");
    let str = "";
    itemjsonarray.forEach((element, index) => {
        str += `
        <tr>
                    <td scope="row">${index+1}</td>
                    <td>${element[0]}</td>
                    <td>${element[1]}</td>
                    <td>${element[2]}</td>
                    <td><button class="btn btn-warning" onclick="deleteitem(${index})">Delete item</button></td>
        </tr>`

    });
    tablebody.innerHTML = str;
    document.getElementById("title").value ="";
    document.getElementById("date").value="";
    document.getElementById("time").value="";
    document.getElementById("description").value="";

})

function update() {
    itemjsonarraystr = localStorage.getItem("itemsjson");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    let tablebody = document.getElementById("tablebody");
    let str = "";
    itemjsonarray.forEach((element, index) => {
        str += `
        <tr>
                    <td scope="row">${index+1}</td>
                    <td>${element[0]}</td>
                    <td>${element[1]}</td>
                    <td>${element[2]}</td>
                    <td><button class="btn btn-warning" onclick="deleteitem(${index})">Delete item</button></td>
        </tr>`

    });
    tablebody.innerHTML = str;
}

function deleteitem(index) {
    itemjsonarraystr = localStorage.getItem("itemsjson");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    itemjsonarray.splice(index, 1);
    localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));
    update();

}

function clearlist() {
    alert("Do you really want to clear your schedules? It can't be reversed.");
    itemjsonarraystr = localStorage.getItem("itemsjson");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    itemjsonarray = [];
    localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));
    let tablebody = document.getElementById("tablebody");
    tablebody.innerHTML = "";
}