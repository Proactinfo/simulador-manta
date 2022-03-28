
$('#btn-search-predios').click(function () {
  localStorage.clear();
  claveCatastral = $("#inputText").val()

  if (!claveCatastral) {
    Swal.fire(
      'Error',
      'Ingrese una Clave Catastral',
      'error' ,
    )
    return;
  }
  getDataByClaveCata(claveCatastral)
  getDataBCByClaveCata(claveCatastral)
  getPhotosByCalveCata(claveCatastral)
  getEdifByClaveCata(claveCatastral)
  localStorage.setItem("temp_new",JSON.stringify(parseFloat(0)));
  localStorage.setItem("temp_old",JSON.stringify(parseFloat(0)));
  localStorage.setItem("temp_inv",JSON.stringify(parseFloat(0)));    

});


$('#btn-mod-pre').click(function () {


  clave = localStorage.getItem("blopr_clave")


  if (clave) {

    $(location).attr('href', '/modificar')
    
  } else {
    Swal.fire(
      'Alerta',
      'Primero busque la Catastral',
      'warning' ,
    )
  }
});

$('#btn-arrow-back').click(() => {
  $(location).attr('href', '/')
  localStorage.clear()
})




const getEdifByClaveCata = (claveCata) => {
  $(`#pills-bp-c > `).remove();
  $(`#pills-tabContent-bp-c > `).remove();

  $.get('/getEdifByClaveCata', { claveCata : claveCata },  (data, status) => {
    resp = JSON.parse(data)
    data_li = ``;
    data_div = ``;
    for (let i = 0; i < resp[1].blopr_num.length; i++) {

      data_li += `<li 
                           class="nav-item" 
                           role="presentation">
                            <a
                               class="nav-link"
                               id="tab-bp-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                               data-mdb-toggle="pill"
                               href="#pills-bp-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                               role="tab"
                            >
                            ${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}
                            </a>
                        </li>`;

      data_div += `<div
                             class="tab-pane fade "
                             id="pills-bp-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                             role="tabpanel">

                        </div>`;

    }
    $(`#pills-bp-c`).append(data_li);
    $(`#pills-tabContent-bp-c`).append(data_div);


    for (let i = 0; i < resp[1].blopr_num.length; i++) {
      data_div_accordion = ``;
      data_div_accordion += `<div 
                                    class="accordion accordion-flush"
                                    id="accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                    </div>`;
      $(`#pills-bp-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(data_div_accordion)

    }

    for (let i = 0; i < resp[1].blopr_num.length; i++) {
      data_div_accordion_ES = ``;
      data_div_accordion_ES += `<div 
                                        class="accordion-item">
                                            <h2 
                                                class="accordion-header" 
                                                id="flush-heading-c-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <button
                                                        class="accordion-button collapsed"
                                                        type="button"
                                                        data-mdb-toggle="collapse"
                                                        data-mdb-target="#flush-collapse-c-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                        aria-controls="flush-collapse-c-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                > 
                                                    Estructuras 
                                                </button>
                                            </h2>
                                            <div
                                                id="flush-collapse-c-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                class="accordion-collapse collapse"
                                                aria-labelledby="flush-heading-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                data-mdb-parent="#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                            >
                                                <div 
                                                    class="accordion-body container"
                                                    id="accordion-body-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <div class="row gx-1">
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Columnas</h5>
                                                      <ul
                                                        id="ul-0201-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Vigas</h5>
                                                      <ul
                                                        id="ul-0202-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Entre</h5>
                                                      <ul
                                                        id="ul-0203-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Paredes</h5>
                                                      <ul
                                                        id="ul-0204-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Escalera</h5>
                                                      <ul
                                                        id="ul-0205-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Cubierta</h5>
                                                      <ul
                                                        id="ul-0206-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                                  </div>
                                                    
            
                                                </div>
                                            </div>
            
                                    </div>`;
      data_div_accordion_AC = ``;
      data_div_accordion_AC += `<div 
                                        class="accordion-item">
                                            <h5 
                                                class="accordion-header" 
                                                id="flush-heading-ac-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <button
                                                        class="accordion-button collapsed"
                                                        type="button"
                                                        data-mdb-toggle="collapse"
                                                        data-mdb-target="#flush-collapse-ac-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                        aria-controls="flush-collapse-ac-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                    > 
                                                    Acabados 
                                                    </button>
                                            </h5>
                                            <div
                                                id="flush-collapse-ac-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                class="accordion-collapse collapse"
                                                aria-labelledby="flush-heading-es-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                data-mdb-parent="#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                            >
                                                <div 
                                                    class="accordion-body container"
                                                    id="accordion-body-ac-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <div class="row gx-1">
                                                    <div class="col-lg-2 col-md-12">
                                                      <h5>Rev. de Pisos</h5>
                                                      <ul
                                                        id="ul-0301-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Rev. Interior</h5>
                                                      <ul
                                                        id="ul-0302-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Rev. Exterior</h5>
                                                      <ul
                                                        id="ul-0303-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Rev. Escalera</h5>
                                                      <ul
                                                        id="ul-0304-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Tumbados</h5>
                                                      <ul
                                                        id="ul-0305-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                                  </div>
                                                  <div class="row gx-1">
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Cubierta</h5>
                                                      <ul
                                                        id="ul-0306-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Puertas</h5>
                                                      <ul
                                                        id="ul-0307-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Ventanas</h5>
                                                      <ul
                                                        id="ul-0308-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-2 col-md-6">
                                                      <h5>Cubre Ventanas</h5>
                                                      <ul
                                                        id="ul-0309-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                                    <div class="col-lg-2 col-md-12">
                                                      <h5>Closets</h5>
                                                      <ul
                                                        id="ul-0310-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                                  </div>
                                                </div>
                                            </div>
            
                                    </div>`;
      data_div_accordion_INS = ``;
      data_div_accordion_INS += `<div 
                                        class="accordion-item">
                                            <h5 
                                                class="accordion-header" 
                                                id="flush-heading-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <button
                                                        class="accordion-button collapsed"
                                                        type="button"
                                                        data-mdb-toggle="collapse"
                                                        data-mdb-target="#flush-collapse-c-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                        aria-controls="flush-collapse-c-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                    > 
                                                    Intalaciones
                                                    </button>
                                            </h5>
                                            <div
                                                id="flush-collapse-c-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                class="accordion-collapse collapse"
                                                aria-labelledby="flush-heading-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                data-mdb-parent="#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                            >
                                                <div 
                                                    class="accordion-body container"
                                                    id="accordion-body-ins-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}">
                                                    <div class="row gx-1">
                                                    <div class="col-lg-3 col-md-6">
                                                      <h5>Sanitarias</h5>
                                                      <ul
                                                        id="ul-0401-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-3 col-md-6">
                                                      <h5>Baños</h5>
                                                      <ul
                                                        id="ul-0402-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-3 col-md-6">
                                                      <h5>Eléctricas</h5>
                                                      <ul
                                                        id="ul-0403-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                              
                                                    <div class="col-lg-3 col-md-6">
                                                      <h5>Cerramientos</h5>
                                                      <ul
                                                        id="ul-0404-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}"
                                                      ></ul>
                                                    </div>
                                                  </div>
                                                </div>
                                            </div>
            
                                    </div>`;


      $(`#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(data_div_accordion_ES)
      $(`#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(data_div_accordion_AC)
      $(`#accordion-c-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(data_div_accordion_INS)

    }


    for (let i = 0; i < resp[1].blopr_num.length; i++) {
      for (let j = 0; j < resp[3].desed_codigo[i].length; j++) {

        if ("0201" == resp[3].desed_codigo[i][j].substr(0, 4)) {

          $(`#ul-0201-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        if ("0202" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0202-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        if ("0203" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0203-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        if ("0204" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0204-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        if ("0205" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0205-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        if ("0206" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0206-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)
        }
        // 
        if ("0301" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0301-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0302" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0302-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0303" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0303-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0304" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0304-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0305" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0305-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0306" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0306-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0307" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0307-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0308" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0308-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0309" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0309-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0310" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0310-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        // 
        if ("0401" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0401-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0402" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0402-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0403" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0403-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }
        if ("0404" == resp[3].desed_codigo[i][j].substr(0, 4)) {
          $(`#ul-0404-${resp[1].blopr_num[i]}-${resp[2].blopr_numpiso[i]}`).append(`<li>${resp[4].desed_descri[i][j]}</li>`)

        }

      }
    }

  });

}

const getPhotosByCalveCata = (claveCata) => {
  $(`#carousel-indicators >`).remove();
  $(`#carousel-inner >`).remove();
  $.get('/getPhotosByClaveCata',
  {claveCata: claveCata },
  function (data, status) {
    resp = JSON.parse(data);
    data_button = ``;
    data_div = ``;


    for (let i = 0; i < resp.count; i++) {


      if (i == 0) {

        data_button += `<button
                                           type="button"
                                           data-mdb-target="#carouselExampleIndicators"
                                           data-mdb-slide-to="${i}"
                                           class="active"
                                   ></button>`;
        data_div += `<div 
                                   class="carousel-item active ">
                                   <img
                                   src="static/predios/${resp.claveCatastral}-${i}.jpg"
                                   class="d-block w-100"
                                   alt="${resp.claveCatastral}-${i}"
                                   />
                               </div>`;
      } else {

        data_button += `<button
                                           type="button"
                                           data-mdb-target="#carouselExampleIndicators"
                                           data-mdb-slide-to="${i}"
                                          
                                   ></button>`;
        data_div += `<div 
                                   class="carousel-item ">
                                   <img
                                   src="static/predios/${resp.claveCatastral}-${i}.jpg"
                                   class="d-block w-100"
                                   alt="${resp.claveCatastral}-${i}"
                                   />
                               </div>`;
      }

    }

    $(`#carousel-indicators`).append(data_button);
    $(`#carousel-inner`).append(data_div);
});
}

const getDataBCByClaveCata = (claveCata) => {
  $.get('/getDataBCByClaveCata', { claveCata: claveCata} , function (data, status) {

    if (status = 'success') {

      resp = JSON.parse(data);

      data_clave = resp[0].pre_codigocatastral
      localStorage.setItem("blopr_clave", JSON.stringify(data_clave));
      if (data_clave) {
        
        data_bloqr = resp[1].blopr_numero[0]
        if (data_bloqr == 0) {
          $('#tabla_predio_pro').attr("hidden", true);

          if ($('table> tbody > tr:first  td').text()) {
            $('table> tbody > tr').remove();
            $('table> tfoot > tr').remove();
            $(`#pills-bp-c > `).remove();
            $(`#pills-tabContent-bp-c > `).remove();

          }

          Swal.fire(
            'No se encontro',
            `${resp.pre_codigocatastral}`,
            'warning'
          )
        } else {
          $('#tabla_predio_pro').attr("hidden", false);

          if ($('table> tbody > tr:first  td').text()) {
            $('table  > tbody > tr').remove();
            $('table  > tfoot > tr').remove();

          }
          var event_data = ``;
          var event_data_total = `<tr>
                                            <th scope="col">Total</th>
                                            <th scope="col"></th>
                                            <th scope="col">${parseFloat(resp[4].SuperfConstrTotal).toLocaleString()} m<sup>2</sup></th>
                                            <th scope="col"></th>
                                            <th scope="col"></th>
                                            <th scope="col">$${parseFloat(resp[10].Total).toLocaleString()}</th>
                                  </tr>`;
          $.each(resp[1].blopr_numero, function (index, value) {
            event_data += `<tr>
                                         <td> ${resp[1].blopr_numero[index]} </td>
                                         <td> ${resp[2].blopr_numpiso[index]} </td>
                                         <td> ${parseFloat(resp[3].blopr_superfconstr[index]).toLocaleString()} m<sup>2</sup>  </td>
                                         <td class="bg-image hover-overlay">$${parseFloat(resp[5].Vm2Rep[index]).toLocaleString()}
                                             <div
                                                class="mask">
                                                <p class="text-success">${resp[6].Vm2Rep_tooltips[index]}</p>
                                                <p class="text-warning">${resp[11].Vm2Rep_tooltipsf}</p>
                                             </div>
                                         </td>
                                         <td class="bg-image hover-overlay">$${parseFloat(resp[7].Vm2Edif[index]).toLocaleString()}
                                             <div
                                                class="mask">
                                                <p class="text-success">${resp[8].Vm2Edif_tooltips[index]}</p>
                                                <p class="text-warning">${resp[12].Vm2Edif_tooltipsf}</p>
                                             </div>
                                         </td>
                                         <td> $${parseFloat(resp[9].ValorEdif[index]).toLocaleString()}</td> 
                           </tr>`;

          });
          $('table> tbody:last').append(event_data);
          $('table> tfoot:last').append(event_data_total);
        }


      }else{
        $('#tabla_predio_pro').attr("hidden", true);

        if ($('table> tbody > tr:first  td').text()) {
          $('table> tbody > tr').remove();
          $('table> tfoot > tr').remove();
          $(`#pills-bp-c > `).remove();
          $(`#pills-tabContent-bp-c > `).remove();

        }

        Swal.fire(
          'No se encontro',
          `${resp.pre_codigocatastral}`,
          'warning'
        )
      }
    }
  });
}

const getDataByClaveCata = (claveCata) =>{
  $.get('/getDataByClaveCata',{claveCata:claveCata});
}













        




 











































