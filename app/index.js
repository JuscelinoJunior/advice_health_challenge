function showOwnerCreateBox() {
  Swal.fire({
    title: 'Add owner',
    html:
      '<input id="id" type="hidden">' +
      '<input id="fname" class="swal2-input" placeholder="First Name">' +
      '<input id="lname" class="swal2-input" placeholder="Last Name">',
    focusConfirm: false,
    preConfirm: () => {
      ownerCreate();
    }
  })
}

function ownerCreate() {
  const first_name = document.getElementById("fname").value;
  const last_name = document.getElementById("lname").value;

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://0.0.0.0:8080/owners");
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify({
    "first-name": first_name, "last-name": last_name
  }));
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      const objects = JSON.parse(this.responseText);
      if (this.status !== 201) {
        Swal.fire({icon: "error", text: objects["detail"]})
      } else {
        Swal.fire({icon: "success", text: "Owner created successfully"});
        loadTable();
      }
    }
  };
}


function showCarCreateBox() {
  Swal.fire({
    title: 'Add car',
    html:
      '<input id="id" type="hidden">' +
      '<label> Model:' +
      '<select id="model" class="swal2-input">' +
        '<option value="hatch">Hatch</option>' +
        '<option value="sedan">Sedan</option>' +
        '<option value="convertible">Convertible</option>' +
      '</select>' +
      '</label>' +
      '<label> Color:' +
      '<select id="color" class="swal2-input">' +
        '<option value="hatch">Yellow</option>' +
        '<option value="sedan">Blue</option>' +
        '<option value="convertible">Green</option>' +
      '</select>' +
      '</label>' +
      '<input id="owner-id" class="swal2-input" placeholder="Owner ID">',
    focusConfirm: false,
    preConfirm: () => {
      carCreate();
    }
  })
}

function carCreate() {
  const model = document.getElementById("model").value;
  const color = document.getElementById("color").value;
  const owner_id = document.getElementById("owner-id").value;

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://0.0.0.0:8080/cars");
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify({
    "model": model, "color": color, "owner-id": Number(owner_id)
  }));
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      const objects = JSON.parse(this.responseText);
      if (this.status !== 201) {
        Swal.fire({icon: "error", text: objects["detail"]})
      } else {
        Swal.fire({icon: "success", text: "Car created successfully"});
        loadTable();
      }
    }
  };
}


function ownerDelete(id) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", "http://0.0.0.0:8080/owners/" + id);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify({
    "id": id
  }));
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      if (this.status !== 204) {
        const objects = JSON.parse(this.responseText);
        Swal.fire({icon: "error", text: objects["detail"]})
      } else {
        Swal.fire({icon: "success", text: "The owner was deleted successfully."});
        loadTable();
      }
    }
  };
}


function carDelete(id) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", "http://0.0.0.0:8080/cars/" + id);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify({
    "id": id
  }));
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      if (this.status !== 204) {
        const objects = JSON.parse(this.responseText);
        Swal.fire({icon: "error", text: objects["detail"]})
      } else {
        Swal.fire({icon: "success", text: "The cara was deleted successfully."});
        loadTable();
      }
    }
  };
}


function loadTable() {
  const xhttp_owners = new XMLHttpRequest();
  xhttp_owners.open("GET", "http://0.0.0.0:8080/owners");
  xhttp_owners.send();
  xhttp_owners.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.responseText);
      var trHTML = '';
      const objects = JSON.parse(this.responseText);
      for (let object of objects) {
        trHTML += '<tr>';
        trHTML += '<td>' + object['id'] + '</td>';
        trHTML += '<td>' + object['first-name'] + '</td>';
        trHTML += '<td>' + object['last-name'] + '</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="ownerDelete(' + object['id'] + ')">Delete</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("onwerstable").innerHTML = trHTML;
    }
  };

  const xhttp_cars = new XMLHttpRequest();
  xhttp_cars.open("GET", "http://0.0.0.0:8080/cars");
  xhttp_cars.send();
  xhttp_cars.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.responseText);
      var trHTML = '';
      const objects = JSON.parse(this.responseText);
      for (let object of objects) {
        trHTML += '<tr>';
        trHTML += '<td>'+object['id']+'</td>';
        trHTML += '<td>'+object['model']+'</td>';
        trHTML += '<td>'+object['color']+'</td>';
        trHTML += '<td>'+object['owner-id']+'</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="carDelete('+object['id']+')">Delete</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("carstable").innerHTML = trHTML;
    }
  };
}

loadTable();