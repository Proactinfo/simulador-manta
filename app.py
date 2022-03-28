import os
from fpdf import FPDF
from datetime import datetime


from flask import Flask, render_template, request, jsonify, make_response, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from controllers.valoracionPredio import ValoracionPredio, valoracionPrediosUrb, valoracionPredioTotal
from controllers.getPrediosValoracion import getEdif, getEdifPredioCod


# nuevas mejoras con las tablas temporales
from controllers.temporales import valoracionTempByClaveCata, setEdifBpTempByClaveCata, setDataBloqPisoByClaveCata, setUpdateDataBloquesByClaveCata,getValTempByCalveCata, getValByCalveCata, getValByCalveCataManta,queryTempDataByClaveCata, getValSueloByPre
# nuevas mejoras valoracion masiva

from database.config import connectionDB

#
from controllers.valoracionMasiva import setValGlobal, upload_file_data, insertTempData,deleteTempData
from controllers.getDataByPredio import getValoracionPredioByClaveCata, getDataEdifByClaveCata
from controllers.getPhotosPredio import getPhotosByClaveCata

from dotenv import load_dotenv

load_dotenv()

PWD = os.get_exec_path()
UPLOAD_FOLDER = os.getcwd()+'/static/uploads'

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def index():
    return(render_template('index.html'))


@app.route("/valoracionIndividual")
def valoracionIndividual():
    return(render_template('valoracionIndividual.html'))


@app.route("/valoracionGrupal")
def valoracionGrupal():
    return(render_template('valoracionGrupal.html'))


@app.route("/modificar")
def modificar():
    return(render_template('modificar.html',token='token'))


@app.route("/importar")
def importar():
    return(render_template('import.html'))


@app.route("/comparacion")
def comparacion():
    return(render_template('comparacion.html'))


@app.route("/importando")
def importando():
    return(render_template('import.html'))


@app.route("/valorar", methods=['POST'])
def valorar():
    if request.method == 'POST':
        text = request.get_json("answer")
        text = text['answer']
        ValoracionPredio(text,  11)
    return 'ok'


@app.route('/pdf/<claveCata>')
def pdfGenerate(claveCata):
    conn = connectionDB()
    cur = conn.cursor()

    # * Fecha
    date = datetime.now()
    # * Clave Catastral
    
    # * Clave Catastral Anterior
    sql_claveAnt = "select p.pre_codigoanterior from predio p where p.pre_codigocatastral = '"+claveCata+"' limit 1;"

    cur.execute(sql_claveAnt)

    data_clavaAnt= cur.fetchall()
    conn.commit()
    # * Detalle : Clave Catastral,Bloque-Piso, Superficie,Year,Estado,Valor old, valor individual, valor modif
    sql_data = "select bp.blopr_numero,  bp.blopr_numpiso, bp.blopr_superfconstr, bp.blopr_anioconstruccion,(select de.desed_descripcion  from desc_edif_bloque_temp deb  left join desc_edificacion_temp de on de.desed_codigo = deb.desed_codigo  where deb.pre_codigocatastral = bp.pre_codigocatastral  and deb.blopr_numero = bp.blopr_numero  and deb.blopr_numpiso = bp.blopr_numpiso  and deb.desed_codigo like '0103%' ) as estado, (select bpt.blopr_valorindividual  from bloques_predio bpt where bpt.pre_codigocatastral = bp.pre_codigocatastral  and bpt.blopr_numero = bp.blopr_numero  and bpt.blopr_numpiso = bp.blopr_numpiso order by bp.blopr_numero ,bp.blopr_numpiso) as valind, (select bpt.blopr_valcomeredifblo  from bloques_predio bpt where bpt.pre_codigocatastral = bp.pre_codigocatastral  and bpt.blopr_numero = bp.blopr_numero  and bpt.blopr_numpiso = bp.blopr_numpiso order by bp.blopr_numero ,bp.blopr_numpiso) as valold, bp.blopr_valcomeredifblo as valnew  from bloques_predio_temp bp where bp.pre_codigocatastral='"+claveCata+"' order by bp.blopr_numero ,bp.blopr_numpiso"
    # * Query DataBase
    cur.execute(sql_data)
    # * Data []
    data = cur.fetchall()
    # * Query complete
    conn.commit()
    # * Query DatosEdificacion 0103 , 02 = Estrutras,03 =Acacados ,04 =Instalaciones
    sql_dataEdifAcaEst = "select deb.pre_codigocatastral,deb.blopr_numero,deb.blopr_numpiso, array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo) where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '01010%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0201%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0202%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0203%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0204%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0205%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0206%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0301%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0302%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0303%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0304%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0305%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0306%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0307%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0308%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0309%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0310%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0401%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0402%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0403%'), array(select de.desed_codigoficha  from desc_edif_bloque_temp deb01 left outer join desc_edificacion_temp de on (de.desed_codigo = deb01.desed_codigo)  where deb01.pre_codigocatastral=deb.pre_codigocatastral and deb01.blopr_numero = deb.blopr_numero and deb01.blopr_numpiso =deb.blopr_numpiso and deb01.desed_codigo like  '0404%') as columnas from  desc_edif_bloque_temp deb where deb.pre_codigocatastral = '"+claveCata+"' group by deb.pre_codigocatastral, deb.blopr_numero, deb.blopr_numpiso order by deb.blopr_numero, deb.blopr_numpiso ;"
    # * Query DataBase
    cur.execute(sql_dataEdifAcaEst)
    # * Data []
    dataEdifAcaEst = cur.fetchall()
    # * Query complete
    conn.commit()
    # * Data Edificacion  [[],[]]
    # TODO : Extraer desde la base de datos
    # TODO : Consulta datos Estructuras , Acabados,Instalaciones

    datosEstAca = [["01 No Tiene", "11 Bloque", "24 Parquet", "34 Fibro Cemento", "48 Aluminio / Vidrio"],
                ["02 Hormigón Armado", "12 Ladrillo", "25 Vinil","35 Fibra Sintética", "49 Granito"],
                ["03 Hormigón Ciclopeo", "13 Piedra", "26 Duela","36 Estucado", "50 Yeso / Cielo Falso"],
                ["04 Hormigón Simple", "17 Arena-Cemento","27 Tablón / Gres", "37 Teja Común", "51 Madera y Vidrio"],
                ["05 Pilotes", "18 Tierra", "28 Tabla","38 Teja Vidriada", "63 Madera y Ladrillo"],
                ["06 Hierro", "19 Mármol", "29 Azulejo","39 Zinc", "66 Piedra o Ladrillo Hornamental"],
                ["07 Estructura Metálica", "20 Marmetón","30 Grafiado", "40 Polietileno", "67 Tol Hierro"],
                ["08 Madera Común", "21 Marmolina", "31 Champeado","41 Domos / Traslúcido", "68 Cemento Alisado"],
                ["09 Caña", "22 Baldosa Cemento", "32 Aluminio","46 Hierro-Madera", "69 Pintado"],
                ["10 Madera Fina", "23 Baldosa Cerámica", "33 Enrollable", "47 Madera Malla", ""]]

    datosIns = [["01 No Tiene","06 Bloque","07 Caña","08 Malla" ,"09 Piedra","10 Ladrillo","11 Madera","12 Metal","52 Letrina" ],
                ["53 Baño Común","54 Medio Baño","55 Un Baño","56 Dos Baños","57 Tres Baños","58 Cuatro Baños","59 + de 4 Baños","62 Empotrado","63 A la vista"]]
    # * Encabezado Tabla Detalle

    head_detalle = ["NO BLOQUE",
                    "NO PISO",
                    "AREA - m2",
                    "AÑO",
                    "ESTADO DE CONSERVACION",
                    "VALOR 2021",
                    "VALOR 2022",
                    "VALOR SIMULADO"]

    # * Encabezado Tabla Edificacion
    head_data = ["No Bloque - No Piso",
                "Estructura",
                "Columnas",
                "Paredes",
                "Vigas",
                "Escalera",
                "Entre Pisos",
                "Cubierta",
                "Rev. de Pisos",
                "Cubierta",
                "Rev. Interior",
                "Puertas",
                "Rev. Exterior",
                "Ventanas",
                "Rev. Escalera",
                "Cubre Ventanas",
                "Tumbados",
                "Closets",
                "Sanitarias",
                "Eléctricas",
                "Baños",
                "Cerramientos"
                ]

    
    sum_m2      = [i[2] for i in data]
    sum_val2021 = [i[5] for i in data]
    sum_val2022 = [i[6] for i in data]
    sum_valSim  = [i[7] for i in data]


    footer_detalle = ["TOTAL",
                    "",
                    sum(sum_m2),
                    "",
                    "",
                    sum(sum_val2021),
                    sum(sum_val2022),
                    sum(sum_valSim) ]



    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ! Header Titulos,Img,Fecha

    # * FOND HEADER TITLE BLOB
    pdf.set_font('Arial', 'B', 10)
    # @param title_header
    # @param path_img_logo
    title_header  = "GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DE MANTA \n"+\
                    "CATASTRO PREDIAL URBANO \n"+\
                    "SIMULADOR DE VALORACION DE EDIFICACION"
    # * HEADER LOGO
    path_img_logo = os.getcwd()+"/static/img/logo_manta.jpg"
    pdf.image(path_img_logo, 10, 11, 19, 19, 'JPG')
    pdf.multi_cell(190, 7, title_header, 1, 'C')


    # * FOND HEADER TITLE FECHA
    pdf.set_font('Arial', '', 8)
    pdf.text(185, 13, str(date.strftime("%m/%d/%y")))

    # ! Header END



    # ! TEXT SECTION BLOD 9
    pdf.set_font('Arial', 'B', 9)
    pdf.text(10, 37.5, '1. CLAVE CATASTRAL:')
    pdf.text(10, 60, '2. DATOS DE LOS BLOQUES CONSTRUCTIVOS')

    pdf.text(25, 43.5, 'CODIGO NACIONAL')
    pdf.text(90, 43.5, 'CODIGO LOCAL')

    pdf.text(160, 43.5, 'CODIGO ANTERIOR')



    # ! TEXT SECTION BLOD 9 FIN

    # ! TEXT SECTION  9
    # * text clave Catastral
    pdf.set_font('Arial', '', 9)
    pdf.text(50, 37.5, claveCata)
    # ! TEXT SECTION  8 FIN

    pdf.cell(190, 25, "", 0, 2)
    
    pdf.set_font('Arial', '', 9)
    # ! CODIGO COMPLETO
    # ! CODIGO NACIONAL
    pdf.text(20.5, 49, claveCata[0:2])
    pdf.text(35.5, 49, claveCata[2:4])
    pdf.text(50.5, 49, claveCata[4:6])
    # ! CODIGO NACIONAL

    pdf.text(70.5 , 49, claveCata[6:8])
    pdf.text(85.5 , 49, claveCata[8:10])
    pdf.text(99.5, 49, claveCata[10:13])
    pdf.text(115.5, 49, claveCata[13:17])
    pdf.text(135.5, 49, claveCata[17:20])

    # ! CODIGO ANTERIOR
    pdf.text(165, 49, data_clavaAnt[0][0])
    
    # ! FOND 6 BLOB CODIGO DESCRIPTION

    pdf.set_font('Arial', '', 7)
    pdf.text(16   , 53.5, 'PROVINCIA')
    pdf.text(32.5 , 53.5, 'CANTON')
    pdf.text(46.5 , 53.5, 'PARROQUIA')
    pdf.text(68.5 , 53.5, 'ZONA')
    pdf.text(82.5 , 53.5, 'SECTOR')
    pdf.text(97   , 53.5, 'MANZANA')
    pdf.text(114.5, 53.5, 'PREDIO')
    pdf.text(132.5, 53.5, 'P.HORIZONTAL')

    # # ? BOX
    pdf.rect(18 , 45.5, 10, 5, 'D')
    pdf.rect(33 , 45.5, 10, 5, 'D')
    pdf.rect(48 , 45.5, 10, 5, 'D')
    pdf.rect(68 , 45.5, 10, 5, 'D')
    pdf.rect(83 , 45.5, 10, 5, 'D')
    pdf.rect(98 , 45.5, 10, 5, 'D')
    pdf.rect(113, 45.5, 15, 5, 'D')
    pdf.rect(133, 45.5, 15, 5, 'D')


    # ! 1.- CLAVE CATASTRAL END
    # ! 2.- DATOS DE BLOS BLOQUES CONSTRUCTIVOS
    pdf.ln(7.5)

    pdf.set_font('Arial', 'B', 7)
    page_width_h = pdf.w - 2 * pdf.l_margin
    col_width_h = page_width_h/8
    th = 5

    pdf.set_x(15)
    pdf.cell(20,  th, str(head_detalle[0]), border=1, ln=0, align='C')
    pdf.cell(15,  th, str(head_detalle[1]), border=1, ln=0, align='C')
    pdf.cell(30,  th, str(head_detalle[2]), border=1, ln=0, align='C')
    pdf.cell(10,  th, str(head_detalle[3]), border=1, ln=0, align='C')
    pdf.cell(37.5,th, str(head_detalle[4]), border=1, ln=0, align='C')
    pdf.cell(col_width_h, th, str(head_detalle[5]), border=1, ln=0, align='C')
    pdf.cell(col_width_h, th, str(head_detalle[6]), border=1, ln=0, align='C')
    pdf.cell(col_width_h, th, str(head_detalle[7]), border=1, ln=0, align='C')
    pdf.ln(th)
    pdf.set_font('Arial', '', 7)
    for i in data:
        pdf.set_x(15)
        pdf.cell(20, th, str(i[0]), border=1,align='C')
        pdf.cell(15, th, str(i[1]), border=1,align='C')
        pdf.cell(30, th, "{:,.4f} m2".format(i[2]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
        pdf.cell(10, th, str(i[3]), border=1,align='C')
        pdf.cell(37.5, th, str(i[4]), border=1,align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(i[5]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(i[6]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(i[7]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
        pdf.ln(th)

    pdf.set_x(15)
    pdf.cell(20, th, str(footer_detalle[0]), border=1, ln=0, align='C')
    pdf.cell(15, th, str(footer_detalle[1]), border=0, ln=0, align='C')
    pdf.cell(30, th, "{:,.4f} m2".format(footer_detalle[2]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
    pdf.cell(10, th, str(footer_detalle[3]), border=0, ln=0, align='C')
    pdf.cell(37.5, th, str(footer_detalle[4]), border=0, ln=0, align='C')
    pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[5]).replace(",", "@").replace(".", ",").replace("@", ".") , border=1, ln=0, align='C')
    pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[6]).replace(",", "@").replace(".", ",").replace("@", ".") , border=1, ln=0, align='C')
    pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[7]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
    pdf.ln(th)

    pdf.ln(1)
    pdf.ln(1)
    pdf.ln(1)


    # ! 2.- DATOS DE BLOS BLOQUES CONSTRUCTIVOS END

    # ! 3.- 3.- DESCRIPCION DE LA EDIFICACION 
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(190,5,"3.-DESCRIPCION DE LA EDIFICACION",0,1,"J")
    
    pdf.cell(190,5,"CODIGO DE EDIFICACION",0,1,"J")

    pdf.set_font('Arial', '', 7)
    pdf.set_x(15)
    pdf.cell(19,5,"01 Aporticado",0,0,"J")
    pdf.cell(16,5,"02 Soporte"   ,0,0,"J")
    pdf.cell(14,5,"03 Mixto"     ,0,0,"J")
    pdf.ln(th)
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(14,5,"ESTRUCTURA Y ACABADOS",0,0,"J")
    pdf.ln(th)
    pdf.set_font('Arial', '', 7)
    for i in datosEstAca:
        pdf.set_x(15)
        pdf.cell(28.5, th, str(i[0]), border=0,align='J')
        pdf.cell(28.5, th, str(i[1]), border=0,align='J')
        pdf.cell(25, th, str(i[2]), border=0,align='J')
        pdf.cell(28.5, th, str(i[3]), border=0,align='J')
        pdf.cell(38.5, th, str(i[4]), border=0,align='J')
        pdf.cell(30, th, str(i[4]), border=0,align='J')
        pdf.ln(th)
    pdf.set_font('Arial', 'B', 8)

    pdf.cell(14,5,"INSTALACIONES",0,0,"J")
    pdf.ln(th)
    pdf.set_font('Arial', '', 7)
    for i in datosIns:
        pdf.set_x(15)
        pdf.cell(20, th, str(i[0]), border=0,align='J')
        pdf.cell(20, th, str(i[1]), border=0,align='J')
        pdf.cell(20, th, str(i[2]), border=0,align='J')
        pdf.cell(20, th, str(i[3]), border=0,align='J')
        pdf.cell(20, th, str(i[4]), border=0,align='J')
        pdf.cell(20, th, str(i[5]), border=0,align='J')
        pdf.cell(20, th, str(i[6]), border=0,align='J')
        pdf.cell(20, th, str(i[7]), border=0,align='J')
        pdf.cell(20, th, str(i[8]), border=0,align='J')
        pdf.ln(th)
        # print(col_width_h)
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.ln(th)
    pdf.ln(th)

    pdf.set_x(50)
    pdf.cell(150, th,"ESTRUCTURA" , border=1, ln=0, align='C')

    pdf.ln(th)
    pdf.cell(25, th, str(head_data[0]), border=1, ln=0, align='C')
    pdf.cell(15, th, str(head_data[1]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[2]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[3]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[4]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[5]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[6]), border=1, ln=0, align='C')
    pdf.cell(25, th, str(head_data[7]), border=1, ln=0, align='C')
    pdf.ln(th)
    for i in dataEdifAcaEst:
        pdf.cell(25, th, str(i[1])+" - "+str(i[2]), border=1,align='C')
        pdf.cell(15, th, str(i[3]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[4]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[5]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[6]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[7]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[8]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.cell(25, th, str(i[9]).replace("[","").replace("]","").replace("'",""), border=1,align="C")
        pdf.ln(th)

    pdf.ln(th)

    pdf.set_x(35)
    pdf.cell(165, th,"ACABADOS" , border=1, ln=0, align='C')
    pdf.ln(th)
    pdf.cell(25, th, str(head_data[0]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[8]), border=1, ln=0, align='C')    
    pdf.cell(14, th, str(head_data[9]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[10]), border=1, ln=0, align='C')    
    pdf.cell(14, th, str(head_data[11]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[12]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[13]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[14]), border=1, ln=0, align='C')    
    pdf.cell(20, th, str(head_data[15]), border=1, ln=0, align='C')    
    pdf.cell(17, th, str(head_data[16]), border=1, ln=0, align='C')    
    pdf.cell(15, th, str(head_data[17]), border=1, ln=0, align='C')  
    pdf.ln(th)
    for i in dataEdifAcaEst:
        pdf.cell(25, th, str(i[1])+" - "+str(i[2]), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[10]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(14, th, str(i[11]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[11]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(14, th, str(i[12]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[13]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[14]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[15]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(20, th, str(i[16]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(17, th, str(i[17]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(15, th, str(i[18]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.ln(th)

    col_width_h = page_width_h/5
    pdf.ln(th)
    pdf.set_x(48)
    pdf.cell(152, th,"INSTALACION" , border=1, ln=0, align='C')
    pdf.ln(th)
    pdf.cell(col_width_h, th, str(head_data[0]) , border=1, ln=0, align='C')    
    pdf.cell(col_width_h, th, str(head_data[18]), border=1, ln=0, align='C')    
    pdf.cell(col_width_h, th, str(head_data[19]), border=1, ln=0, align='C')    
    pdf.cell(col_width_h, th, str(head_data[20]), border=1, ln=0, align='C') 
    pdf.cell(col_width_h, th, str(head_data[21]), border=1, ln=0, align='C') 

    pdf.ln(th)

    for i in dataEdifAcaEst:
        pdf.cell(col_width_h, th, str(i[1])+" - "+str(i[2]) , border=1, ln=0, align='C')    
        pdf.cell(col_width_h, th, str(i[19]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(col_width_h, th, str(i[20]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C')    
        pdf.cell(col_width_h, th, str(i[21]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C') 
        pdf.cell(col_width_h, th, str(i[22]).replace("[","").replace("]","").replace("'",""), border=1, ln=0, align='C') 
        pdf.ln(th)
    # ! 3.- 3.- DESCRIPCION DE LA EDIFICACION EN

    cur.close()
    conn.close()
    # attachment
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'inline;attachment='+claveCata+'.pdf'})


@app.route("/getPredioUrb")
def getPredioUrb():
    return valoracionPrediosUrb()


@app.route("/getValoracionManta")
def getValoracionManta():
    return valoracionPredioTotal()


#
# ! Valoiracion Masiva

@app.route('/deleteAllDataTemp',methods=['GET'])
def deleteAllData():
    if request.method == 'GET':
        return deleteTempData()
        
@app.route("/insertAllDataTemp", methods=['GET'])
def insertAllData():
    if request.method == 'GET':
        return insertTempData()

@app.route("/valAllDataTemp", methods=['GET'])
def valAllDataTemp():
    if request.method == 'GET':
        return setValGlobal()

@app.route('/pdfGAD',methods=['GET'])
def pdfGAD():
    if request.method  == 'GET':
        conn = connectionDB()
        cur = conn.cursor()


        # * consulta Sql

        sql =("select p.divpo_codigo,"
              +"dp.divpo_nombre,"
              +"count(1) as predios,"
              +"sum(bp.blopr_superfconstr) as superficie, " 
              +"sum(bp.blopr_valorindividual) as val2021, "
              +"sum(bp.blopr_valcomeredifblo) as val2022, "
              +"sum(bpt.blopr_valcomeredifblo)as valSimul "		
              +"from bloques_predio bp "
              +"left outer join predio p on (p.pre_codigocatastral = bp.pre_codigocatastral) "
              +"left outer join bloques_predio_temp bpt on (bpt.pre_codigocatastral = bp.pre_codigocatastral) "
              +"left outer join division_politica dp on (dp.divpo_codigo = p.divpo_codigo) "
              +"where p.pre_estado = 'A' and p.pre_tipo = 'Urbano' "
              +"group by p.divpo_codigo, dp.divpo_nombre "
              +"order by p.divpo_codigo;")

        cur.execute(sql)


        data = cur.fetchall()
        
        sum_predios     = [ i[2] for i in data]
        sum_superficie  = [ i[3] for i in data]
        sum_val2021     = [ i[4] for i in data]
        sum_val2022     = [ i[5] for i in data]
        sum_valSim      = [ i[6] for i in data]
        
        footer_detalle = ["TOTAL",
                            sum(sum_predios),
                            sum(sum_superficie),
                            sum(sum_val2021),
                            sum(sum_val2022),
                            sum(sum_valSim) ]

        

        conn.commit()
        # * Encavezado Tabla Valoraciion Parroquial

        head_detalle = [
                        "PARROQUIA",
                        "No PREDIOS",
                        "SUPERFICE",
                        "VALOR 2021",
                        "VALOR 2022",
                        "VALOR SIMULADO"
                        ]

        pdf = FPDF()
        
        # * Fecha
        date = datetime.now()

        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial','B',10)

        # ! Header Titulos,Img,Fecha

        # * FOND HEADER TITLE BLOB
        pdf.set_font('Arial', 'B', 10)
        # @param title_header
        # @param path_img_logo
        title_header  = "GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DE MANTA \n"+\
                        "CATASTRO PREDIAL URBANO \n"+\
                        "VALOR SIMULADO DE EDIFICACION"
        # * HEADER LOGO
        path_img_logo = os.getcwd()+"/static/img/logo_manta.jpg"
     
        pdf.image(path_img_logo, 10, 11, 19, 19, 'JPG')
        pdf.multi_cell(190, 7, title_header, 1, 'C')


        # * FOND HEADER TITLE FECHA
        pdf.set_font('Arial', '', 8)
        pdf.text(185, 13, str(date.strftime("%m/%d/%y")))

        # ! 2.  Descripcion de la edifiacion
        pdf.set_font('Arial', 'B', 9)
        pdf.ln(5)
        pdf.cell(190,5,"1. VALOR DE EDIFICACION POR PARROQUIA",0,1,"J")
        pdf.ln(5)
    

        pdf.set_font('Arial', 'B', 7)
        page_width_h = pdf.w - 2 * pdf.l_margin
        col_width_h = page_width_h/6
        th = 5

        
        pdf.cell(col_width_h, th, str(head_detalle[0]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, str(head_detalle[1]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, str(head_detalle[2]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, str(head_detalle[3]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, str(head_detalle[4]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, str(head_detalle[5]), border=1, ln=0, align='C')
        pdf.ln(th)
        
        
        for i in data:
            pdf.cell(col_width_h, th, str((i[1],"SANTA MARIANITA")[i[1]=="SANTA MARIANITA (BOCA DE PACOCHE)"]), border=1,align='C')
            pdf.cell(col_width_h, th, "{:,.2f} ".format(i[2]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
            pdf.cell(col_width_h, th, "{:,.4f} ".format(i[3]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
            pdf.cell(col_width_h, th, "{:,.2f} ".format(i[4]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
            pdf.cell(col_width_h, th, "{:,.2f} ".format(i[5]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
            pdf.cell(col_width_h, th, "{:,.2f} ".format(i[6]).replace(",", "@").replace(".", ",").replace("@", "."), border=1,align='C')
            pdf.ln(th)
        pdf.cell(col_width_h, th, str(footer_detalle[0]), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, "{:,.2f} ".format(footer_detalle[1]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, "{:,.4f} m2".format(footer_detalle[2]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[3]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[4]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
        pdf.cell(col_width_h, th, "$ {:,.2f}".format(footer_detalle[5]).replace(",", "@").replace(".", ",").replace("@", "."), border=1, ln=0, align='C')
        cur.close()
        conn.close()
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'inline;attachment=valoracionParroquial.pdf'})
            

# ! Valoiracion Masiva End


@app.route("/getPredioUrbManta", methods=['GET'])
def getPredioUrbManta():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getValByCalveCataManta(claveCata)


# ! MODULO INVIDUAL -> /valoracionIndividual

# ? Complete getDataBCByClaveCata ->  obtener informacion valorada por Clave Catastal
@app.route("/getDataBCByClaveCata", methods=['GET'])
def getDataBCByClaveCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getValoracionPredioByClaveCata(claveCata)

# ? Complete getPhotosByClaveCata ->  Datos imagenes por  ID - ClaveCatastral


@app.route("/getPhotosByClaveCata", methods=['GET'])
def getPhotosPreCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getPhotosByClaveCata(claveCata)

# ? Complete getEdifByClaveCata -> Datos Edicacion por  ID - ClaveCatastral
@app.route("/getEdifByClaveCata", methods=['GET'])
def getEdifByClaveCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
    return getDataEdifByClaveCata(claveCata)

# ! END MODULO INVIDUAL -> /valoracionIndividual

# ! MODULO INVIDUAL -> /modificar

# ? Complete table Datps Edif view
@app.route("/getEdifCod", methods=['GET'])
def getEdifCod():
    if request.method == 'GET':
        return getEdif()

@app.route("/edifPredioCod", methods=['GET'])
def edifPredioCod():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getEdifPredioCod(claveCata)

# obtener informacion de la clave Catastral Bloque-Piso :
@app.route('/getDataBPByClaveCata', methods=['GET'])
def getDataBPByClaveCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return setDataBloqPisoByClaveCata(claveCata)

# TODO : uploadBloqByClaveCata
# send data temp

@app.route('/uploadBloqByClaveCata', methods=['POST'])
def saveBloqByClaveCata():
    if request.method == 'POST':
        pre_codigocatastral = request.get_json("pre_codigocatastral")
        pre_codigocatastral = pre_codigocatastral['pre_codigocatastral']

        bloq_piso = request.get_json('bloq_piso')
        bloq_piso = bloq_piso['bloq_piso']
        
        bloq_num = request.get_json('bloq_num')
        bloq_num = bloq_num['bloq_num']

        blopr_superfconstr = request.get_json("blopr_superfconstr")
        blopr_superfconstr = blopr_superfconstr['blopr_superfconstr']

        blopr_anioconstruccion = request.get_json("blopr_anioconstruccion")
        blopr_anioconstruccion = blopr_anioconstruccion['blopr_anioconstruccion']

        desed_codigo = request.get_json("desed_codigo")
        desed_codigo = desed_codigo['desed_codigo']

        return setUpdateDataBloquesByClaveCata(pre_codigocatastral, bloq_piso,bloq_num, blopr_superfconstr, blopr_anioconstruccion, desed_codigo)


# ! END MODULO INVIDUAL -> /modificar

@app.route("/getValSueloByClaveCata",methods=["GET"])
def getValSueloByClaveCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getValSueloByPre(claveCata)
#  Query data por ID


@app.route("/getDataByClaveCata", methods=['GET'])
def getDataByClaveCata():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return queryTempDataByClaveCata(claveCata)

# Query Valoracion


@app.route('/getDataValByClaveCata', methods=['GET'])
def getDataVal():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getValByCalveCata(claveCata)

# Query Valoracion Simulador


@app.route('/getDataTempValByClaveCata', methods=['GET'])
def getDataTempVal():
    if request.method == 'GET':
        claveCata = request.values.get('claveCata')
        return getValTempByCalveCata(claveCata)


# Valoracion por ID - ClaveCatastral
@app.route("/valTempByClaveCata", methods=['POST'])
def valTempByClaveCata():
    if request.method == 'POST':
        text = request.get_json("claveCata")
        text = text['claveCata']
        return valoracionTempByClaveCata(text)



# Datos temporales edificacion por clave catastral
@app.route("/edifBpTempByClaveCata", methods=['POST'])
def edifBpTempByClaveCata():
    if request.method == 'POST':
        text_ClaveCata = request.get_json("ClaveCata")
        text_ClaveCata = text_ClaveCata['ClaveCata']
        text_BloqCata = request.get_json("BloqCata")
        text_BloqCata = text_BloqCata['BloqCata']
        tex_BloqPisoCata = request.get_json("BloqPisoCata")
        tex_BloqPisoCata = tex_BloqPisoCata['BloqPisoCata']
        tex_DesedCodigo = request.get_json("DesedCodigo")
        tex_DesedCodigo = tex_DesedCodigo['DesedCodigo']
        setEdifBpTempByClaveCata(
            text_ClaveCata, text_BloqCata, tex_BloqPisoCata, tex_DesedCodigo)
        return 'ok'

# * Sucess
@app.route('/uploader', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_file_data(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('valoracionGrupal.html')
    else:
        resp = jsonify(
            {'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            debug=os.getenv('DEBUG'),
            )
