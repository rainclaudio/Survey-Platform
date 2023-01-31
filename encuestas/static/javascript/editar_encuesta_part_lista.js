console.log("hola mundo");

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
function extract_info(list_Node_HTML) {
  var div_name = list_Node_HTML.getElementsByTagName("div")[1];
  var name = div_name.getElementsByTagName("h5")[0].innerText;
  var email = div_name.getElementsByTagName("span")[0].innerText;
  var image_file = list_Node_HTML
    .getElementsByTagName("img")[0]
    .currentSrc.split("profile_pics/")[1];
  return {
    name: name,
    email: email,
    image_file: image_file,
  };
}

async function get_and_send_request(encuesta_id, list_Node_HTML) {
  var info_user = extract_info(list_Node_HTML);
  console.log("INFO COMPLETA");
  console.log(info_user);

  // TASK: ENVIAR USUARIO PARA ASOCIARLO A UNA INVITACIÓN DE UNA ENCUESTA
  // LA RUTA AUN NO ESTA CREADA
  var dataReply = await request({
    method: "POST",
    url: "/add_invitado_encuesta",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      encuesta_id: encuesta_id,
      name: info_user.name,
      email: info_user.email,
      image_file: info_user.image_file,
    }),
  });
}

async function remove_user(user_id, encuesta_id) {
  console.log(user_id);
  var invited_user_li = document.getElementById(`invited-user-${user_id}`);
  invited_user_li.remove();

  var dataReply = await request({
    method: "POST",
    url: "/delete_user_of_encuesta",
    headers: ["Content-type", "application/x-www-form-urlencoded"],
    body: JSON.stringify({
      somedata: "data",
      user_id: user_id,
      encuesta_id: encuesta_id,
    }),
  });
}

function add_users(encuesta_id, users_list, lista_id) {
  var users_to_invite = users_list.getElementsByTagName("li");
  var users_already_invited;
  if (document.getElementById("users-invited") == null) {
    console.log(document.getElementById("users-invited"));
  } else {
    users_already_invited = document
      .getElementById("users-invited")
      .getElementsByTagName("li");
  }

  console.log(users_already_invited);
  // get ids de usuarios ya invitados
  var invited_user_ids = [];
  if (users_already_invited != null) {
    for (var i = 0; i < users_already_invited.length; ++i) {
      var invited_user_id =
        +users_already_invited[i].id.split("invited-user-")[1];
      invited_user_ids.push(invited_user_id);
    }
  }
  // agregar a usuarios que aun no han sido invitados
  for (var i = 0; i < users_to_invite.length; ++i) {
    var user_to_invite = +users_to_invite[i].id.split(
      "lista-" + lista_id + "-user-"
    )[1];

    if (!invited_user_ids.includes(user_to_invite)) {
      get_and_send_request(encuesta_id, users_to_invite[i]);

      var createLi = document.createElement("li");
      createLi.id = "invited-user-" + user_to_invite;
      // createLi.classList.add(users_to_invite[i].classList);
      createLi.innerHTML = users_to_invite[i].innerHTML;
      createLi.classList = "d-flex justify-content-between";
      createLi.insertAdjacentHTML(
        "beforeend",
        ` <div onclick="remove_user(${user_to_invite}, ${encuesta_id})">
      <svg
        version="1.1"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        width="15px"
        height="15px"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g transform="matrix(1 0 0 1 -253 -7 )">
          <path
            d="M 14.6464646464646 11.2121212121212  C 14.8821548821549 11.4478114478114  15 11.7340067340067  15 12.0707070707071  C 15 12.4074074074074  14.8821548821549 12.6936026936027  14.6464646464646 12.9292929292929  L 12.9292929292929 14.6464646464646  C 12.6936026936027 14.8821548821549  12.4074074074074 15  12.0707070707071 15  C 11.7340067340067 15  11.4478114478114 14.8821548821549  11.2121212121212 14.6464646464646  L 7.5 10.9343434343434  L 3.78787878787879 14.6464646464646  C 3.55218855218855 14.8821548821549  3.26599326599327 15  2.92929292929293 15  C 2.59259259259259 15  2.30639730639731 14.8821548821549  2.07070707070707 14.6464646464646  L 0.353535353535354 12.9292929292929  C 0.117845117845118 12.6936026936027  0 12.4074074074074  0 12.0707070707071  C 0 11.7340067340067  0.117845117845118 11.4478114478114  0.353535353535354 11.2121212121212  L 4.06565656565657 7.5  L 0.353535353535354 3.78787878787879  C 0.117845117845118 3.55218855218855  0 3.26599326599327  0 2.92929292929293  C 0 2.59259259259259  0.117845117845118 2.3063973063973  0.353535353535354 2.07070707070707  L 2.07070707070707 0.353535353535354  C 2.30639730639731 0.117845117845117  2.59259259259259 0  2.92929292929293 0  C 3.26599326599327 0  3.55218855218855 0.117845117845117  3.78787878787879 0.353535353535354  L 7.5 4.06565656565657  L 11.2121212121212 0.353535353535354  C 11.4478114478114 0.117845117845117  11.7340067340067 0  12.0707070707071 0  C 12.4074074074074 0  12.6936026936027 0.117845117845117  12.9292929292929 0.353535353535354  L 14.6464646464646 2.07070707070707  C 14.8821548821549 2.3063973063973  15 2.59259259259259  15 2.92929292929293  C 15 3.26599326599327  14.8821548821549 3.55218855218855  14.6464646464646 3.78787878787879  L 10.9343434343434 7.5  L 14.6464646464646 11.2121212121212  Z "
            fill-rule="nonzero"
            fill="#d7d7d7"
            stroke="none"
            transform="matrix(1 0 0 1 253 7 )"
          />
        </g>
      </svg>
    </div>`
      );
      // var new_invited = users_to_invite[i];
      // new_invited.id = "invited-user-" + user_to_invite;
      console.log("es nulo");
      if (users_already_invited != null) {
        document.getElementById("users-invited").appendChild(createLi);
      }
    }
  }
}

function add_list_to_invited(encuesta_id, lista_id) {
  users_list = document.getElementById(`users-of-${lista_id}`);
  if (users_list != null) {
    users = add_users(encuesta_id, users_list, lista_id);
  }
}
