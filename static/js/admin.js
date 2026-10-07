const search = document.getElementById("search");

const tableBody = document.getElementById("tableBody");

search.addEventListener("keyup", function(){

    const value = this.value.toLowerCase();

    const rows = tableBody.getElementsByTagName("tr");

    for(let row of rows){

        const username =
            row.cells[1].innerText.toLowerCase();

        row.style.display =
            username.includes(value)
            ? ""
            : "none";
    }

});