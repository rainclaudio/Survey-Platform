/************************************/
/*           Request function       */
/************************************/

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
  const icon_close = `<ion-icon onclick="delete_item('${pregunta_id}','${dataReply.id}');" id="close_${pregunta_id}-item_${dataReply.id}" class= "text-white bg-danger" name="close-outline"></ion-icon>`;
  li_element.insertAdjacentHTML("beforeend", icon_close);

  // Insert
  items_preg.appendChild(li_element);
  return dataReply;
}

/************************************/
/*           DELETE ITEM            */
/************************************/

function delete_item(pregunta_id, item_id) {
  console.log(item_id);
  // PREPARANDO INFORMACIÔN
  var xml = new XMLHttpRequest();
  dataSend = JSON.stringify({
    somedata: "data",
    item_id: item_id,
  });
  xml.open("POST", `/delete_item_test`, true);
  xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  // RECIBIENDO RESPUESTA
  xml.onload = function () {
    var dataReply = JSON.parse(this.responseText);
    console.log(dataReply);
    const exact_icon_close = document.getElementById(
      `close_${pregunta_id}-item_${item_id}`
    );
    console.log(exact_icon_close);
    exact_icon_close.parentElement.remove();
  };

  console.log(dataSend);
  // ENVIANDO RESPUESTA
  xml.send(dataSend);
}
