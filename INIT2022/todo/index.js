add = document.getElementById("add");
add.addEventListener("click", () => {
    title = document.getElementById("title").value;
    des = document.getElementById("description").value;
    if (localStorage.getItem("itemsjson") == null) {
        itemjsonarray = [];
        itemjsonarray.push([title, des]);
        localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));

    } else {
        itemjsonarraystr = localStorage.getItem("itemsjson");
        itemjsonarray = JSON.parse(itemjsonarraystr);
        itemjsonarray.push([title, des]);
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
                    <td><button class="btn btn-warning" onclick="deleteitem(${index})">Delete item</button></td>
        </tr>`

    });
    tablebody.innerHTML = str;

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
    alert("Do you really want to clear your todo list?");
    itemjsonarraystr = localStorage.getItem("itemsjson");
    itemjsonarray = JSON.parse(itemjsonarraystr);
    itemjsonarray = [];
    localStorage.setItem("itemsjson", JSON.stringify(itemjsonarray));
    let tablebody = document.getElementById("tablebody");
    tablebody.innerHTML = "";
}