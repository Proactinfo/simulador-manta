

$('#label_claveCata').append(JSON.parse(localStorage.getItem("blopr_clave")));



const viewDataEdif = () => {


  $.get('/getEdifCod', function (data, status) {

    resp = JSON.parse(data);
    $.get('/edifPredioCod',
    { claveCata: JSON.parse(localStorage.getItem("blopr_clave")) }
      , function (data, status) {

        data_li_es = ``
        data_div_es = ``

        data_li_ac = ``
        data_div_ac = ``

        data_li_ins = ``
        data_div_ins = ``

        resp_bp = JSON.parse(data);
        for (let i = 0; i < resp_bp[1].blopr_numero.length; i++) {


          data_li_es += `<li 
                            class="nav-item ">
                            <a 
                              class="nav-link"
                              id="pills-bp-es-tab-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              data-mdb-toggle="pill"
                              href="#pills-bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              role="tab"
                            >${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}</a>
                        </li>`;

          data_div_es += `<div
                              class="tab-pane"
                              id="pills-bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              role="tabpanel">
                          </div>`;

          data_li_ac += `<li 
                            class="nav-item">
                            <a 
                              class="nav-link"
                              id="pills-bp-ac-tab-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              data-mdb-toggle="pill"
                              href="#pills-bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              role="tab"
                            >${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}</a>
                        </li>`;
          data_div_ac += `<div
                                class="tab-pane"
                                id="pills-bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                                role="tabpanel">
                          </div>`;

          data_li_ins += `<li 
                            class="nav-item">
                            <a 
                              class="nav-link"
                              data-mdb-toggle="pill"
                              id="pills-bp-ins-tab-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              href="#pills-bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              role="tab"
                            >${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}</a>
                        </li>`;
          data_div_ins += `<div
                              class="tab-pane"
                              id="pills-bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}"
                              role="tabpanel">
                        </div>`;
        }

        // add Estructuras
        $('#pills-bp-es').append(data_li_es)
        $('#pills-tabContent-bp-es').append(data_div_es)

        // add Acabados
        $('#pills-bp-ac').append(data_li_ac)
        $('#pills-tabContent-bp-ac').append(data_div_ac)

        // add Instalaciones
        $('#pills-bp-ins').append(data_li_ins)
        $('#pills-tabContent-bp-ins').append(data_div_ins)


        for (let i = 0; i < resp_bp[1].blopr_numero.length; i++) {
          data_total_es = ``;
          data_total_ac = ``;
          data_total_ins = ``;
          for (let j = 0; j < resp[0].desed_codigo.length; j++) {
            // Estructuras
            if ('0201' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Columnas') {
                data_total_es += `<div>
                                        <h3>${resp[2].desed_descripcion[j]}</h3>
                                  </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class ="form-check-input" 
                                      type  ="checkbox" 
                                      name  ="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id    ="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value ="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label 
                                      class="form-check-label"
                                      >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }
            }
            if ('0202' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Vigas y Cadenas') {

                data_total_es += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0203' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Entre Pisos') {

                data_total_es += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0204' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Paredes') {

                data_total_es += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0205' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Escalera') {

                data_total_es += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0206' == resp[0].desed_codigo[j].substr(0, 4)) {
              if (resp[2].desed_descripcion[j] == 'Cubierta') {

                data_total_es += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_es += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            // Acabados
            if ('0301' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Rev. de Pisos') {

                data_total_ac += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0302' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Rev. Interior') {

                data_total_ac += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0303' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Rev. Exterior') {

                data_total_ac += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0304' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Rev. Escalera') {

                data_total_ac += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                > ${resp[2].desed_descripcion[j]}</label>
                          </div>`;
              }

            }
            if ('0305' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Tumbados') {

                data_total_ac += `<div>
                <h3>${resp[2].desed_descripcion[j]}</h3>
              </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0306' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Cubierta') {

                data_total_ac += `<div>
                                  <h3>${resp[2].desed_descripcion[j]}</h3>
                             </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label 
                                      class="form-check-label"
                                      >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0307' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Puertas') {

                data_total_ac += `<div>
                                    <h3>${resp[2].desed_descripcion[j]}</h3>
                             </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label 
                                      class="form-check-label"
                                      >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0308' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Ventanas') {

                data_total_ac += `<div>
                                  <h3>${resp[2].desed_descripcion[j]}</h3>
                             </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0309' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Cubre Ventanas') {

                data_total_ac += `<div>
                                  <h3>${resp[2].desed_descripcion[j]}</h3>
                            </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label class="form-check-label"
                                >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }
            if ('0310' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Closets') {

                data_total_ac += `<div>
                                  <h3>${resp[2].desed_descripcion[j]}</h3>
                            </div>`
              } else {
                data_total_ac += `<div 
                                class="form-check">
                                <input 
                                      class="form-check-input" 
                                      type="checkbox" 
                                      name="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      id="bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                      value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                <label 
                                      class="form-check-label"
                                      >
                                ${resp[2].desed_descripcion[j]}
                                </label>
                          </div>`;
              }

            }

            // Instalaciones

            if ('0401' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Sanitarias') {

                data_total_ins += `<div>
                  <h3>${resp[2].desed_descripcion[j]}</h3>
                </div>`
              } else {
                data_total_ins += `<div 
                                  class="form-check">
                                  <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        name="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        id="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                  <label class="form-check-label"
                                  >
                                  ${resp[2].desed_descripcion[j]}
                                  </label>
                            </div>`;
              }

            }
            if ('0402' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Baños') {

                data_total_ins += `<div>
                  <h3>${resp[2].desed_descripcion[j]}</h3>
                </div>`
              } else {
                data_total_ins += `<div 
                                  class="form-check">
                                  <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        name="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        id="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                  <label class="form-check-label"
                                  >
                                  ${resp[2].desed_descripcion[j]}
                                  </label>
                            </div>`;
              }

            }
            if ('0403' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Eléctricas') {

                data_total_ins += `<div>
                  <h3>${resp[2].desed_descripcion[j]}</h3>
                </div>`
              } else {
                data_total_ins += `<div 
                                  class="form-check">
                                  <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        name="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        id="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                  <label class="form-check-label"
                                  >
                                  ${resp[2].desed_descripcion[j]}
                                  </label>
                            </div>`;
              }

            }
            if ('0404' == resp[0].desed_codigo[j].substr(0, 4)) {

              if (resp[2].desed_descripcion[j] == 'Cerramientos') {

                data_total_ins += `<div>
                  <h3>${resp[2].desed_descripcion[j]}</h3>
                </div>`
              } else {
                data_total_ins += `<div 
                                  class="form-check">
                                  <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        name="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        id="bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" 
                                        value="${resp_bp[1].blopr_numero[i].length > 1 ? resp_bp[1].blopr_numero[i] : '0' + resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i].length > 1 ? resp_bp[2].blopr_numpiso[i] : '0' + resp_bp[2].blopr_numpiso[i]}-${resp[0].desed_codigo[j]}" >
                                  <label class="form-check-label"
                                  > ${resp[2].desed_descripcion[j]}</label>
                            </div>`;
              }

            }

          }
          $(`#pills-bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}`).append(data_total_es);
          $(`#pills-bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}`).append(data_total_ac);
          $(`#pills-bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}`).append(data_total_ins);

        }

        for (let i = 0; i < resp_bp[1].blopr_numero.length; i++) {
          for (let j = 0; j < resp_bp[3].desed_codigo[i].length; j++) {
            $(`#bp-es-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp_bp[3].desed_codigo[i][j]}`).attr('checked', true);
            $(`#bp-ac-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp_bp[3].desed_codigo[i][j]}`).attr('checked', true);
            $(`#bp-ins-${resp_bp[1].blopr_numero[i]}-${resp_bp[2].blopr_numpiso[i]}-${resp_bp[3].desed_codigo[i][j]}`).attr('checked', true);

          }
          // 
        }
      });

    $.get('/getDataBPByClaveCata',
    { claveCata: JSON.parse(localStorage.getItem("blopr_clave")) },
      function (data, status) {
        resp_data = JSON.parse(data);
        console.log(resp_data);
        data_li_blo = ``
        data_div_blo = ``

        for (let i = 0; i < resp_data[1].blopr_num.length; i++) {


          data_li_blo += `<li 
                              class="nav-item">
                              <a 
                                class="nav-link"
                                id="pills-bp-blo-tab-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                                data-mdb-toggle="pill"
                                href="#pills-bp-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                                role="tab"
                              >${resp_data[1].blopr_num[i].toString().length > 1 ? resp_data[1].blopr_num[i] : '0' + resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i].length > 1 ? resp_data[2].blopr_numpiso[i] : '0' + resp_data[2].blopr_numpiso[i]}</a>
                          </li>`;
          data_div_blo += `<div
                                        class="tab-pane"
                                        id="pills-bp-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                                        role="tabpanel">
                                  </div>`;


        }
        $('#pills-bp-blo').append(data_li_blo)
        $('#pills-tabContent-bp-blo').append(data_div_blo)

        dataForm = ``

        for (let i = 0; i < resp_data[1].blopr_num.length; i++) {

          dataForm += `<div id='formDataBloques-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}' class="row g-3">`

          dataForm += `<div class="col-md-3">
                        <label for="input-m2-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}" class="form-label">Area de construcción - m2:</label>
                        <input type="number" class="form-control" 
                        id="input-m2-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                        name="input-m2-blo"
                        >
                      </div>`;

          dataForm += `<div class="col-md-3">
                        <label for="input-year-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}" class="form-label">Año construcción:</label>
                        <input type="number" class="form-control" 
                        id="input-year-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                        name="input-year-blo"
                        >
                      </div>`;

          dataForm += `<div class="col-md-4">
                        <label for="select-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}" class="form-label">Estado de conservación:</label>
                        <select 
                            id="select-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}"
                            name="select-blo"
                            class="form-select">
                            <option id="select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-010301" value="010301">Nuevo</option>
                            <option id="select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-010302" value="010302">Conservación normal</option>
                            <option id="select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-010303" value="010303">Necesita reparos simples</option>
                            <option id="select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-010304" value="010304">Necesita reparos importantes</option>
                            <option id="select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-010305" value="010305">Para demolición</option>
                        </select>
                      </div>
                      </div>`;

          

          $(`#pills-bp-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}`).append(dataForm);

          dataForm = ``
        }

        for (let i = 0; i < resp_data[1].blopr_num.length; i++) {

          $(`#input-m2-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}`).val(`${resp_data[3].blopr_superfconstr[i]}`)
          $(`#input-year-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}`).val(`${resp_data[4].blopr_anioconstruccion[i]}`)

          $(`#select-op-blo-${resp_data[1].blopr_num[i]}-${resp_data[2].blopr_numpiso[i]}-${resp_data[5].desed_codigo[i]}`).attr('selected', true);

        }


      }
    )



  })

}



$('#btn-back').click(function () {


  clave = localStorage.getItem("blopr_clave")


  if (clave) {
    localStorage.clear();
    $(location).attr('href', '/valoracionIndividual')

  } else {
    localStorage.clear();
    $(location).attr('href', '/valoracionIndividual')
  }
});


$('#btn-save').click(function () {


  bq_num         = []
  bq_numpiso     = []
  bloqNum       = []
  bloqPiso       = []
  desed_codigo   = []
  input_m2_blo   = []
  input_year_blo = []
  select_bloq    = []

  $(`input:checkbox:checked`).each(function () {
    bq_num.push($(this).val().substr(0, 2)[0] == '0' ? $(this).val().substr(0, 2)[1] : $(this).val().substr(0, 2))
    bq_numpiso.push($(this).val().substr(3, 2)[0] == '0' ? $(this).val().substr(3, 2)[1] : $(this).val().substr(3, 2))
    desed_codigo.push($(this).val().substr(6, 6))
  }
  )

  $(`#pills-tabContent-bp-blo`).children().each(function(){
    
    num_temp = $(this).attr('id').substr(13,5)
    
    // console.log(num_temp[1]=='-'," - ", );
    bloqNum.push(num_temp[1] == '-' ? parseInt(num_temp.substr(0,1)) : parseInt(num_temp.substr(0,2)))
    bloqPiso.push(num_temp[1] == '-' ? parseInt(num_temp.substr(2,3)) : parseInt(num_temp.substr(3,6)));
  })


  $(`input[name="input-m2-blo"]`)
        .each(function () {input_m2_blo.push(parseFloat($(this).val())) });
  $(`input[name="input-year-blo"]`)
        .each(function () {input_year_blo.push(parseInt($(this).val())) });
  $(`select[name="select-blo"]`)
        .each(function () {select_bloq.push($(this).val()) });


  $.post('/uploadBloqByClaveCata',JSON.stringify({
    pre_codigocatastral: JSON.parse(localStorage.getItem("blopr_clave")),
    bloq_num :bloqNum ,
    bloq_piso: bloqPiso ,
    blopr_superfconstr:input_m2_blo ,
    blopr_anioconstruccion:input_year_blo  ,
    desed_codigo:select_bloq
  }));
  


  $.post('/edifBpTempByClaveCata',
    JSON.stringify({
      ClaveCata: JSON.parse(localStorage.getItem("blopr_clave")),
      BloqCata: bq_num,
      BloqPisoCata: bq_numpiso,
      DesedCodigo: desed_codigo,
    })
    , function (data, status) {
      $.post('/valTempByClaveCata',JSON.stringify({claveCata:JSON.parse(localStorage.getItem("blopr_clave"))}),function(){
        Swal.fire(
          'Tarea Completa',
          'Datos Guardados',
          'success' ,
        )
      })
    });
});






$(document).ready(
  () => {

    viewDataEdif();

  });





