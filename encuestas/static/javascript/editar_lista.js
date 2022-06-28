/*********************************************************************/
/*                        Request function                          */
/********************************************************************/
// Se comunica con la base de datos de flask a través de una ruta.
// obj contiene la información necesaria (metodo,headers,JSON a enviar)
function request(obj) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    // Abrir request: Método y url
    xhr.open(obj.method || "GET", obj.url);
    // Añadir Headers
    if (obj.headers) {
      Object.keys(obj.headers).forEach((key) => {
        xhr.setRequestHeader(key, obj.headers[key]);
      });
    }
    // Luego de envío...
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 400) {
        // If response is all good...
        return resolve(JSON.parse(xhr.responseText));
      } else {
        alert("there was an error");
        return reject("error");
      }
    };
    // Enviar
    xhr.send(obj.body);
  });
}
/********************************************************************/
/*                      Funciones Iniciales                         */
/********************************************************************/
// Añaden funcionalidad a la edición del
//título de la encuesta,preguntas y
//descripción de los items cuando estos son renderizados por primera vez
document.querySelectorAll(".title").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo editar título encuesta: " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("lista_")[1]);
    var dataReply_updt_item = await update_title_list(
      encuesta.id.split("lista_")[1],
      encuesta.value
    );
  });
});
document.querySelectorAll(".description").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo editar description encuesta: " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("lista_descr_")[1]);
    var dataReply_updt_item = await update_descr_list(
      encuesta.id.split("lista_descr_")[1],
      encuesta.value
    );
  });
});

async function update_title_list(encuesta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/update_title_list",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      lista_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}
async function update_descr_list(encuesta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/update_description_list",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      lista_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}
async function select_user(user_id, lista_id) {
  row_user = document.getElementById(`user_${user_id}`);
  row_user.remove();

  var dataReply = await request({
    method: "POST",
    url: "/add_user_in_list",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      user_id: user_id,
      lista_id: lista_id,
    }),
  });

  button_remove = document.createElement("button");
  button_remove.textContent = "Eliminar";
  button_remove.onclick = function () {
    remove_user(user_id, lista_id);
  };
  cells_of_row = row_user.getElementsByTagName("td");
  last_cell = cells_of_row[cells_of_row.length - 1];
  last_cell.innerHTML = "";
  last_cell.appendChild(button_remove);

  console.log(last_cell);
  users_in_list = document.getElementById("users-in-list");
  users_in_list.appendChild(row_user);
}
async function remove_user(user_id, lista_id) {
  row_user = document.getElementById(`user_${user_id}`);

  var dataReply = await request({
    method: "POST",
    url: "/delete_user_in_list",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      somedata: "data",
      user_id: user_id,
      lista_id: lista_id,
    }),
  });
  button_add = document.createElement("button");
  button_add.textContent = "Añadir";
  button_add.onclick = function () {
    select_user(user_id, lista_id);
  };
  cells_of_row = row_user.getElementsByTagName("td");
  last_cell = cells_of_row[cells_of_row.length - 1];
  last_cell.innerHTML = "";
  last_cell.appendChild(button_add);

  row_user.remove();
  users_in_list = document.getElementById("total-users");
  users_in_list.appendChild(row_user);
}
