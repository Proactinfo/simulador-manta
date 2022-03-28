$.get("/getPredioUrb", function (data, status) {
  $('#spinner1').hide();
  $('#spinner2').hide();
  $('#spinner3').hide();
  $('#spinner4').hide();
  $('#spinner5').hide();
  
  resp = JSON.parse(data);
  var event_data = ``;
  data_resp = resp[0].divpo_nombre

  var event_data_total = `<tr>
    <th scope="col">Total</th>
    <th scope="col">${parseFloat(resp[4].sum_predios).toLocaleString()}</th>
    <th scope="col">${parseFloat(resp[5].sum_superfconstr).toLocaleString()} m<sup>2</sup></th>
    <th scope="col">$ ${parseFloat(resp[6].sum_valedif).toLocaleString()}</th>
    </tr>`;
    
  $.each(data_resp, function (index, value) {

    event_data += `<tr>
        <td> ${resp[0].divpo_nombre[index]} </td>
        <td> ${parseFloat(resp[1].predios[index]).toLocaleString()} </td>
        <td> ${parseFloat(resp[2].superfconstr[index]).toLocaleString()}  m<sup>2</sup> </td>
        <td> ${parseFloat(resp[3].valedif[index]).toLocaleString()} </td>
     </tr>`;

  })
  $('#tabla_predio_pro_urb>table> tbody:last').append(event_data);
  $('#tabla_predio_pro_urb>table> tfoot:last').append(event_data_total);
});

$("#recalcular").on('click', function () {
  $('#spinner1').show();
  $('#spinner2').show();
  $('#spinner3').show();
  $('#spinner4').show();
  $('#spinner5').show();

  $.get('/insertAllDataTemp', (data, status) => {

    resp_insert = JSON.parse(data)
    if (resp_insert.success == 'ok') {

      $.get("/valAllDataTemp", function (data, status) {
        
        resp  = JSON.parse(data)
        if (resp.message == true) {
          $('#spinner1').hide();
          $('#spinner2').hide();
          $('#spinner3').hide();
          $('#spinner4').hide();
          $('#spinner5').hide();
        }
      });
    }
  })
});


$(`#btn-upload-excel`).click(async () => {

  const { value: file } = await Swal.fire({
    title: 'Select excel',
    input: 'file',
    inputAttributes: {
      'accept': '*',
      'aria-label': 'Upload your excel file'
    }
  })

  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      print(e)
      Swal.fire({
        title: 'Your uploaded file',

      })
    }
    reader.readAsDataURL(file)
  }

})


$('#btn-back').click(() => {

  $.get('/deleteAllDataTemp');

  $(location).attr('href', '/')
});
