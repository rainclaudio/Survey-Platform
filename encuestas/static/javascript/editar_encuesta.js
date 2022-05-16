/************************************/
/*           Funciones Iniciales    */
/************************************/

/* Añaden funcionalidad a la edición del 
título de la encuesta,preguntas y 
descripción de los items */
document.querySelectorAll(".title-encuesta").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log("has dejado el encuesta " + encuesta.value);
    console.log("el encuesta id: ", encuesta.id.split("encuesta_")[1]);
    var dataReply_updt_item = await update_title(
      encuesta.id.split("encuesta_")[1],
      encuesta.value
    );
  });
});
document.querySelectorAll(".pregunta-encuesta").forEach((pregunta) => {
  pregunta.addEventListener("blur", async function () {
    console.log("has dejado el pregunta " + pregunta.value);
    console.log("el pregunta id: ", pregunta.id.split("pregunta_")[1]);
    var dataReply_updt_item = await update_pregunta(
      pregunta.id.split("pregunta_")[1],
      pregunta.value
    );
  });
});
document.querySelectorAll(".item-preg").forEach((item) => {
  item.addEventListener("blur", async function () {
    console.log("has dejado el item " + item.value);
    console.log("el item id: ", item.id.split("item_")[1]);
    var dataReply_updt_item = await update_item(
      item.id.split("item_")[1],
      item.value
    );
  });
});

/************************************/
/*           Request function       */
/************************************/
/*esta es la que se comunica con la BD Flask */
function request(obj) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open(obj.method || "GET", obj.url);
    if (obj.headers) {
      Object.keys(obj.headers).forEach((key) => {
        xhr.setRequestHeader(key, obj.headers[key]);
      });
    }

    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 400) {
        // If response is all good...
        return resolve(JSON.parse(xhr.responseText));
      } else {
        alert("there was an error");
        return reject("error");
      }
    };
    xhr.send(obj.body);
  });
}

/************************************/
/*           ADD input form         */
/************************************/
async function update_pregunta(pregunta_id, description) {
  var dataReply = await request({
    method: "POST",
    url: "/update_pregunta_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      pregunta_id: pregunta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}

async function update_title(encuesta_id, description) {
  var dataReply = await request({
    method: "POST",
    url: "/update_title_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      encuesta_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}

async function update_item(item_id, description) {
  var dataReply = await request({
    method: "POST",
    url: "/update_item_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      item_id: item_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}
/**************************/
/*Manipulación de la DOM */
/**************************/
async function add_input_form(pregunta_id) {
  console.log(pregunta_id);
  var items_preg = document.getElementById(`list_of_${pregunta_id}`);
  var countChilds = items_preg.childElementCount;
  // Create list child
  var li_element = document.createElement("li");

  li_element.classList.add("d-flex", "gap-3", "align-items-center");
  const icon_elipse = `<ion-icon name="ellipse-outline"></ion-icon>`;
  li_element.insertAdjacentHTML("afterbegin", icon_elipse);

  // Create Input
  var input = document.createElement("input");
  input.type = "text";
  input.value = `Alternativa ${countChilds + 1}`;
  input.classList.add(
    "item-preg",
    "w-85",
    "border-left-0",
    "border-right-0",
    "border-top-0"
  );

  var dataReply = await request({
    method: "POST",
    url: "/add_item_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: input.value,
      pregunta_id: pregunta_id,
    }),
  });

  input.addEventListener("blur", async function () {
    var dataReply_updt_item = await update_item(dataReply.id, input.value);
  });

  li_element.appendChild(input);
  const icon_close = `<ion-icon onclick="delete_item('${pregunta_id}','${dataReply.id}',true);" id="close_${pregunta_id}-item_${dataReply.id}" class= "text-white bg-danger" name="close-outline"></ion-icon>`;
  li_element.insertAdjacentHTML("beforeend", icon_close);
  li_element.id = dataReply.id;
  // Insert
  items_preg.appendChild(li_element);
  return dataReply;
}

/************************************/
/*           DELETE ITEM            */
/************************************/

async function delete_item(pregunta_id, item_id, from_delete_item) {
  console.log(item_id);
  // PREPARANDO INFORMACIÔN
  if (from_delete_item) {
    var exact_icon_close = document.getElementById(
      `close_${pregunta_id}-item_${item_id}`
    );
    exact_icon_close.parentElement.remove();
  }
  var dataReply = await request({
    method: "POST",
    url: "/delete_item_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      somedata: "data",
      item_id: item_id,
    }),
  });
}
async function delete_pregunta(pregunta_id, encuesta_id) {
  // 1) Conseguir a los Hijos
  const list = document.getElementById(`list_of_${pregunta_id}`);
  var element_of_lists = list.getElementsByTagName("li");
  // 2) Eliminar a los hijos
  for (let i = 0; i < element_of_lists.length; i++) {
    await delete_item(pregunta_id, element_of_lists[i].id, false);
  }
  // 3) Eliminar al padre

  var xml = new XMLHttpRequest();
  dataSend = JSON.stringify({
    somedata: "data",
    pregunta_id: pregunta_id,
  });
  xml.open("POST", `/delete_pregunta_test`, true);
  xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  // RECIBIENDO RESPUESTA
  xml.onload = function () {
    var dataReply = JSON.parse(this.responseText);
    console.log(dataReply);
    const exact_preg_container = document.getElementById(
      `container_of_${pregunta_id}`
    );
    console.log(exact_preg_container);
    exact_preg_container.remove();
  };

  console.log(dataSend);
  // ENVIANDO RESPUESTA
  xml.send(dataSend);
}

/************************************/
/*           INSERT PREGUNTA        */
/************************************/
async function add_pregunta(encuesta_id) {
  console.log(encuesta_id);
  const add_pregunta_button = document.getElementById("addPregunta");
  // 1) Crear Content Section
  var div_content_section = document.createElement("div");
  var menu_options = document.createElement("div");
  var div_container = document.createElement("div");

  div_content_section.classList.add("content-section", "w-85");
  div_container.classList.add("d-flex");
  // 2) Crear La pregunta
  var dataReply = await request({
    method: "POST",
    url: "/add_pregunta_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: "Título de pregunta",
      encuesta_id: encuesta_id,
    }),
  });
  div_container.id = `container_of_${dataReply.id}`;

  // 3) Crear fieldset e input
  var field_set = document.createElement("fieldset");
  var input = document.createElement("input");

  field_set.classList.add("form-group", "mb-2");
  input.classList.add(
    "pregunta-encuesta",
    "w-100",
    "border-left-0",
    "border-right-0",
    "border-top-0",
    "bg-transparent",
    "outline-none"
  );
  input.id = `pregunta_${dataReply.id}`;
  input.type = "text";
  input.value = dataReply.description;
  input.addEventListener("blur", async function () {
    console.log("has dejado el pregunta " + this.value);
    console.log("el pregunta id: ", this.id.split("pregunta_")[1]);
    var dataReply_updt_item = await update_pregunta(
      this.id.split("pregunta_")[1],
      this.value
    );
  });
  field_set.appendChild(input);
  div_content_section.appendChild(field_set);
  // 4) Añadir el ul
  var ul = document.createElement("ul");
  ul.id = `list_of_${dataReply.id}`;
  ul.classList.add("list-unstyled", "d-flex", "gap-3", "flex-column");
  div_content_section.appendChild(ul);
  // 5) Añadir el botón
  var button = document.createElement("button");
  button.classList.add(
    "d-block",
    "p-1",
    "bg-info",
    "text-white",
    "text-center",
    "w-25"
  );
  button.onclick = function () {
    add_input_form(dataReply.id);
  };
  button.textContent = "Añadir Item";
  menu_options.insertAdjacentHTML(
    "afterbegin",
    ` <div class="h-50 p-3   d-flex  align-items-center border-bottom">
        <ion-icon  onclick="delete_pregunta(${dataReply.id}, ${encuesta_id})" name = "trash"></ion-icon>
      </div>
      <div class="h-50 p-3 d-flex  align-items-center">
        <ion-icon class onclick="" name = "color-wand-outline"></ion-icon>
      </div>`
  );
  console.log(menu_options);
  var content = document.getElementById("content-section");
  div_content_section.appendChild(button);
  div_container.appendChild(div_content_section);
  div_container.insertAdjacentHTML(
    "beforeend",
    `<div class="content-section p-0 d-flex flex-column "> <div class="h-50 p-3   d-flex  align-items-center border-bottom">
  <ion-icon  onclick="delete_pregunta(${dataReply.id}, ${encuesta_id})" name = "trash"></ion-icon>
</div>
<div class="h-50 p-3 d-flex  align-items-center">
  <ion-icon class onclick="" name = "color-wand-outline"></ion-icon>
</div></div>`
  );
  content.insertBefore(div_container, add_pregunta_button);
}
