
console.log( document.querySelectorAll(".dropdown-toggle") );
console.log('hola')
document.querySelectorAll(".dropdown-toggle").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo categoría " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("encuesta_c")[1]);
    var dataReply_updt_item = await update_cat(
      encuesta.id.split("encuesta_c")[1],
      encuesta.value
    );
  });
});

async function update_cat(encuesta_id, categoria) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/update_categoria_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      categoria: categoria,
      encuesta_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}


$(".dropdown-menu li a").click(function(){
  
  var selText = $(this).text();
  update_cat('{{encuesta.id}}',selText )
  console.log(selText)
  $(this).parents('.dropdown').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});


/********************************************************************/
/*                      Funciones Iniciales                         */
/********************************************************************/
// Añaden funcionalidad a la edición del
//título de la encuesta,preguntas y
//descripción de los items cuando estos son renderizados por primera vez


document.querySelectorAll(".title-encuesta").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo editar título encuesta: " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("encuesta_")[1]);
    var dataReply_updt_item = await update_title(
      encuesta.id.split("encuesta_")[1],
      encuesta.value
    );
  });
});
document.querySelectorAll(".description-encuesta").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo editar description encuesta: " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("encuesta_descr_")[1]);
    var dataReply_updt_item = await update_descr_encuesta(
      encuesta.id.split("encuesta_descr_")[1],
      encuesta.value
    );
  });
});
document.querySelectorAll(".pregunta-encuesta").forEach((pregunta) => {
  pregunta.addEventListener("blur", async function () {
    console.log("has dejado el campo editar título pregunta" + pregunta.value);
    console.log("el pregunta id: ", pregunta.id.split("pregunta_")[1]);
    var dataReply_updt_item = await update_pregunta(
      pregunta.id.split("pregunta_")[1],
      pregunta.value
    );
  });
});
document.querySelectorAll(".item-preg").forEach((item) => {
  item.addEventListener("blur", async function () {
    console.log("has dejado el campo editar item " + item.value);
    console.log("el item id: ", item.id.split("item_")[1]);
    var dataReply_updt_item = await update_item(
      item.id.split("item_")[1],
      item.value
    );
  });
});
document.querySelectorAll(".image_of_encuesta").forEach((item) => {
  item.addEventListener("change", async function () {
    console.log("has dejado el campo editar item " + item.files[0].name);
    console.log("el item id: ", item.id.split("image_of_encuesta_")[1]);
    var parts_iamge = item.files[0].name.split(".");

    let form = document.createElement("form");
    let input_fake = document.createElement("input");
    input_fake.type = "text";
    input_fake.value = item.id.split("image_of_encuesta_")[1];
    input_fake.name = "static_id";
    form.appendChild(item);
    form.appendChild(input_fake);
    console.log(form);
    form.enctype = "multipart/form-data";
    let formData = new FormData(form);
    console.log(formData);
    // formData.append("photo", item.files[0]);
    var dataReply_updt_item = await update_image_encuesta(
      item.id.split("image_of_encuesta_")[1],
      formData
    );
  });
});
document.querySelectorAll(".posttime-encuesta").forEach((encuesta) => {
  encuesta.addEventListener("blur", async function () {
    console.log(
      "has dejado el campo editar posttime encuesta: " + encuesta.value
    );
    console.log("el encuesta id: ", encuesta.id.split("post_time_")[1]);
    var dataReply_updt_item = await update_post_time(
      encuesta.id.split("post_time_")[1],
      encuesta.value
    );
  });
});
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
/*********************************************************************/
/*                        Actualizaciones de campos                  */
/********************************************************************/
// Aquí se actualizan las preguntas,el título de la encuesta y los items
// Es código repetitivo
async function update_pregunta(pregunta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la pregunta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
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
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
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
async function update_descr_encuesta(encuesta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/update_description_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      encuesta_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}
async function update_image_encuesta(encuesta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de item y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/save_image_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: description,
  });
  console.log(dataReply);
  return dataReply;
}
async function update_item(item_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de item y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
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
async function update_post_time(encuesta_id, description) {
  // NOTAR EL AWAIT: significa que espera hasta que se complete la request antes de seguir con el código
  // Toma el id de la encuesta y lo actualiza
  // LUEGO; ir a la DOM y cambiar el objeto
  var dataReply = await request({
    method: "POST",
    url: "/update_post_time_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: description,
      encuesta_id: encuesta_id,
    }),
  });
  console.log(dataReply);
  return dataReply;
}

/*********************************************************************/
/*                        Eliminación de campos                  */
/********************************************************************/
// Lo que hacen es eliminar primero los campos de la página para luego proceder
// a mandar una request a la base de datos para eliminarlos allí también
async function delete_item(pregunta_id, item_id, from_delete_item) {
  // Elminando de la DOM
  if (from_delete_item) {
    var exact_icon_close = document.getElementById(
      `close_${pregunta_id}-item_${item_id}`
    );
    exact_icon_close.parentElement.remove();
  }
  // Enviando request
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
  // Esta función es más compleja puesto que debemos elminar también a los hijos
  // de una pregunta. Los pasos están especificados
  // 1) Conseguir a los Hijos
  const list = document.getElementById(`list_of_${pregunta_id}`);
  var element_of_lists = list.getElementsByTagName("li");
  // 2) Eliminar a los hijos
  // NOTAR EL AWAIT: Elimino primero a los hijos y luego ejecuto el resto del código
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
/*********************************************************************/
/*                        Add ITEM                                   */
/********************************************************************/
// Aquí vamos a añadir el elemento ITEM a la página
async function add_input_form(pregunta_id) {
  // 1) Conseguimos a los hijos previos de la pregunta, es decir los items, ya cargados
  var items_preg = document.getElementById(`list_of_${pregunta_id}`);
  // 2) Contamos cuantos son
  var countChilds = items_preg.childElementCount;
  // 3) Creamos un elemento tipo li: "elemento de lista"
  var li_element = document.createElement("li");
  // 4) Le añadimos el estilo
  li_element.classList.add("d-flex", "gap-3", "align-items-center");
  // 5) Creamos el icono
  const icon_elipse = `<ion-icon name="ellipse-outline"></ion-icon>`;
  // 6) Lo insertamos en li
  li_element.insertAdjacentHTML("afterbegin", icon_elipse);
  // 7) Create Input
  var input = document.createElement("input");
  // 8) Añadir configuraciones y estilos
  input.type = "text";
  input.value = `Alternativa ${countChilds + 1}`;
  input.classList.add("item-preg", "w-85", "border-0", "border-left-0");
  // 9) Mandamos una request a la base de datos para insertar el campo Item
  //    Notar el body: contiene la descripción y pregunta id
  var dataReply = await request({
    method: "POST",
    url: "/add_item_test",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      description: input.value,
      pregunta_id: pregunta_id,
    }),
  });
  // 10) Le añadimos un evento al input de manera que si lo editamos
  //     Mandemos esa actualización a la base de datos
  input.addEventListener("blur", async function () {
    var dataReply_updt_item = await update_item(dataReply.id, input.value);
  });
  // 11) Añadimos el input a li
  li_element.appendChild(input);
  // 12) añadir el icono junto con la id
  const icon_close = `<ion-icon onclick="delete_item('${pregunta_id}','${dataReply.id}',true);" id="close_${pregunta_id}-item_${dataReply.id}" class= "text-white bg-danger" name="close-outline"></ion-icon>`;
  li_element.insertAdjacentHTML("beforeend", icon_close);
  li_element.id = dataReply.id;
  // 13) añadir el camo li a la lista
  items_preg.appendChild(li_element);
  return dataReply;
}
/************************************/
/*           INSERT PREGUNTA        */
/************************************/
// Insetar una pregunta a la página y mandar la solicitud de inserción
async function add_pregunta(encuesta_id) {
  // Este es el botón azul que aparece al final
  const add_pregunta_button = document.getElementById("addPregunta");
  // 1) Crear Container, contiene a los dos de abajo
  var div_container = document.createElement("div");
  // 2) Opciones menú parte derecha
  // No ES USADA PERO Sí o Sí entra la parte derecha del menú
  // Se reemplaza por el paso 7)
  var menu_options = document.createElement("div");
  // 3) Item Pregunta con alternativas a la izquierda
  var div_content_section = document.createElement("div");
  // 4) Adición de estilo
  div_content_section.classList.add("content-section", "w-85");
  div_container.classList.add("d-flex");
  // 5) Crear la pregunta
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
  // 6) Creando Campos de la pregunta: Título,alternativas y botón: "añadir item"
  // 6.1) Creación Título de pregunta: fieldset e input
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
  // 6.2) Creando parte para guardar las alternativas de las preguntas
  var ul = document.createElement("ul");
  ul.id = `list_of_${dataReply.id}`;
  ul.classList.add("list-unstyled", "d-flex", "gap-3", "flex-column");
  div_content_section.appendChild(ul);
  // 6.3) Creando parte añadir items
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
  div_content_section.appendChild(button);

  div_container.appendChild(div_content_section);
  var content = document.getElementById("content-section");
  // 7) Creando parte derecha: esto fue más rápido porque decubrí que se puede copiar y pegar
  //    Esto reemplaza al menu porque se puede insertar solo directamente y no delgarlo a una variable
  //    (i.e no se puede hacer insertAdjHTML("beforeend", menu_options))
  div_container.insertAdjacentHTML(
    "beforeend",
    `<div class="content-section p-0 d-flex flex-column "> <div class="h-50 p-3   d-flex  align-items-center border-bottom">
  <ion-icon  onclick="delete_pregunta(${dataReply.id}, ${encuesta_id})" name = "trash"></ion-icon>
</div>
<div class="h-50 p-3 d-flex  align-items-center">

</div></div>`
  );
  content.insertBefore(div_container, add_pregunta_button);
}

//Función que revisa cada un minuto para publicar

window.setInterval(function (hora, minutos) {
  var date = new Date();
  if (date.getHours() >= hora && date.getMinutes() >= minutos) {
    if (encuesta.estado == "creada") {
      //publicar (no cacho como)
      alert("hola pooo"); //esto no va
    }
  }
}, 60000); //60000 milisegundos (1 minuto)
