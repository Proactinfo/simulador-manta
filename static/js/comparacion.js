$('#label_claveCata').append(JSON.parse(localStorage.getItem("blopr_clave")));


$(`#back-val-ind`).click(function(){
    localStorage.clear();
})

function porcentaje() {
    
   
    temp_inv    = parseFloat(localStorage.getItem("temp_inv"))
    temp_new    = parseFloat(localStorage.getItem("temp_new"))
    temp_old    = parseFloat(localStorage.getItem("temp_old"))

    val_ant     = parseFloat((((temp_old - temp_inv) /temp_old)*100).toFixed(2)).toString()
    val_new     = parseFloat((((temp_new - temp_inv) /temp_new)*100).toFixed(2)).toString()

    $(`#bg-val-ant`).append(`${val_ant}%`);
    $(`#bg-val-mod`).append(`${val_new}%`);

    
    
}

let area_comunal_mnt = 0 ;



$(document).ready(
    () => {
  
        viewValoracionManta();
        viewValoracion();
        viewValoracionSimulador();
        viewValSueldo();
        
});


const viewValoracionSimulador = () =>{
    $('#valPredioNew').attr("hidden", false)
    $('#valPredioTableNew').attr("hidden", false)
    $.get('/getDataTempValByClaveCata',{ claveCata: JSON.parse(localStorage.getItem("blopr_clave")) },function name(data,status) {
        resp = JSON.parse(data);
        console.log(area_comunal_mnt);
        var event_data = ``;


        var event_data_total = `<tr>
                                    <th scope="col">Total</th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col">$ ${parseFloat(resp[8].Total).toLocaleString()}</th>
                                </tr>`;

        localStorage.setItem("temp_new",JSON.stringify(parseFloat(resp[8].Total)));
        data_resp = resp[5].blopr_valcomeredifblo;
        $.each(data_resp, function (index, value) {
            
            event_data += `<tr>
                               <td> ${resp[1].blopr_numero[index]} </td>
                               <td> ${resp[2].blopr_numpiso[index]} </td>
                               <td> ${parseFloat(resp[3].blopr_superfconstr[index]).toLocaleString()} m<sup>2</sup></td>
                               <td> $ ${parseFloat(resp[4].blopr_valcomerm2[index]).toLocaleString()} </td>
                               <td> ${resp[6].blopr_anioconstruccion[index]} </td> 
                               <td> ${resp[7].estado[index]} </td> 
                               <td> $ ${parseFloat(resp[5].blopr_valcomeredifblo[index]).toLocaleString()} </td> 
                            </tr>`;
        });


        $('#valPredioTableNew> tbody:last').append(event_data);
        $('#valPredioTableNew> tfoot:last').append(event_data_total);
        porcentaje();

    })
}
  

const viewValoracion  = () =>{

    $('#valPredioOld').attr("hidden", false)
    $('#valPredioTableOld').attr("hidden", false)

    $.get('/getDataValByClaveCata',{ claveCata: JSON.parse(localStorage.getItem("blopr_clave")) },function name(data,status) {
        resp = JSON.parse(data);

        var event_data = ``;


        var event_data_total = `<tr>
                                    <th scope="col">Total</th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col"></th>
                                    <th scope="col">$ ${parseFloat(resp[8].Total).toLocaleString()}</th>
                                </tr>`;

        localStorage.setItem("temp_old",JSON.stringify(parseFloat(resp[8].Total)));
        data_resp = resp[5].blopr_valcomeredifblo;
        $.each(data_resp, function (index, value) {
            
            event_data += `<tr>
                               <td> ${resp[1].blopr_numero[index]} </td>
                               <td> ${resp[2].blopr_numpiso[index]} </td>
                               <td> ${parseFloat(resp[3].blopr_superfconstr[index]).toLocaleString()} m<sup>2</sup></td>
                               <td> $ ${parseFloat(resp[4].blopr_valcomerm2[index]).toLocaleString()} </td>
                               <td> ${resp[6].blopr_anioconstruccion[index]} </td> 
                               <td> ${resp[7].estado[index]} </td> 
                               <td> $ ${parseFloat(resp[5].blopr_valcomeredifblo[index]).toLocaleString()} </td> 
                            </tr>`;
        });


        $('#valPredioTableOld> tbody:last').append(event_data);
        $('#valPredioTableOld> tfoot:last').append(event_data_total);


    })
}
  
  
const viewValoracionManta = ()=>{

    $('#valPredioManta').attr("hidden", false)
    $('#valPredioTableManta').attr("hidden", false)
    $.get('/getPredioUrbManta', { claveCata: JSON.parse(localStorage.getItem("blopr_clave")) },function name(data,status) {
            
            resp = JSON.parse(data);



            var event_data = ``;

            area_comunal_mnt = parseFloat(resp[9].sum_blopr_valorcomunal);


            var event_data_total = `<tr>
                                    <th scope="col">Total</th>
                                    <th scope="col"></th>
                                    <th scope="col">${parseFloat(resp[6].sum_blopr_areacomunal).toLocaleString()} m<sup>2</sup> </th>
                                    <th scope="col">${parseFloat(resp[7].sum_blopr_superfconstr).toLocaleString()} m<sup>2</sup> </th>
                                    <th scope="col">$ ${parseFloat(resp[8].sum_blopr_valorindividual).toLocaleString()}</th>
                                    <th scope="col">$ ${parseFloat(resp[9].sum_blopr_valorcomunal).toLocaleString()}</th>
                                    </tr>`;

                                    
                                    
                                    
                                    
            localStorage.setItem("temp_inv",JSON.stringify(parseFloat(resp[8].sum_blopr_valorindividual)));            
            data_resp = resp[0].blopr_numero


            $.each(data_resp, function (index, value) {

                event_data += `<tr>
                                   <td> ${resp[0].blopr_numero[index]} </td>
                                   <td> ${resp[1].blopr_numpiso[index]} </td>
                                   <td> ${parseFloat(resp[2].blopr_areacomunal[index]).toLocaleString()}   m<sup>2</sup> </td>
                                   <td> ${parseFloat(resp[3].blopr_superfconstr[index]).toLocaleString()}  m<sup>2</sup> </td>
                                   <td> $ ${parseFloat(resp[4].blopr_valorindividual[index]).toLocaleString()}</td> 
                                   <td> $ ${parseFloat(resp[5].blopr_valorcomunal[index]).toLocaleString()}</td> 
                                </tr>`;
                             
                                
                                
                                
                                
                                
            });

            
        $('#valPredioTableManta> tbody:last').append(event_data);
        $('#valPredioTableManta> tfoot:last').append(event_data_total);
                 
    });
}


const viewValSueldo = ()=>{
    $.get("/getValSueloByClaveCata",
    { claveCata: JSON.parse(localStorage.getItem("blopr_clave")) }, function name(data , status){

        resp = JSON.parse(data);

        console.log(resp);

        $('#label_valSuelo').append('$ '+resp.val_predio);


        
    })
}
$("#btn-download").attr(
    "href",
    `/pdf/${JSON.parse(localStorage.getItem("blopr_clave"))}`
  );