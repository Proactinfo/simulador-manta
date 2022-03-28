import json
import pandas as pd
from database.config import connectionDB

def setValGlobal():

    conn = connectionDB()
    cur  = conn.cursor()

    sql = "call valPreMaxUrb(2);"
    
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()
    return json.dumps({"message":True})

   

def insertTempData():
    conn = connectionDB()
    cur  = conn.cursor()
    
    cur.execute("DELETE FROM bloques_predio_temp;")
    conn.commit()
    cur.execute("DELETE FROM desc_edif_bloque_temp;")
    conn.commit()

    insertBpTempByClave = "INSERT INTO bloques_predio_temp SELECT pre_codigocatastral,blopr_numero,blopr_superfconstr,blopr_rtipoconstr,blopr_edadconstr,blopr_edadreparacion,blopr_numpisos,blopr_sumatindic,blopr_valm2reps,blopr_valcomerm2,blopr_valcomeredifblo,blopr_porcentajereparacion,blopr_enconstruccion,blopr_anioconstruccion,blopr_aniofinalprevisto,pro_codigo,usu_codigo,sys_period,blopr_numpiso,blopr_fechaingreso,blopr_fechaactualizacion,pisau_codigo,fecha_creacion,blopr_codigoinicial,blopr_censo,blopr_constr_valorarea,blopr_constr_valorareareal,blopr_ph_areacomunal,blopr_ph_valorm2,blopr_ph_valorcomunalm2,blopr_ph_avaluoconstr,blopr_ph_avaluoconstrcomunal,blopr_ph_areaconstr,blopr_ph_areaterrazas,blopr_ph_arealibres,blopr_valorindividual,blopr_valorcomunal,blopr_tipologia,blopr_tipologiaproact,blopr_areacomunal FROM bloques_predio;"
    
    cur.execute(insertBpTempByClave)
    conn.commit()

    insertDescEdifBpByClave = "INSERT INTO desc_edif_bloque_temp SELECT pre_codigocatastral,blopr_numero,desed_codigo, blopr_numpiso  FROM desc_edif_bloque"

    cur.execute(insertDescEdifBpByClave)
    conn.commit()

    cur.close()
    conn.close()

    return json.dumps({
        "success":'ok'
    })

def deleteTempData():
    conn = connectionDB()
    cur  = conn.cursor()
    
    cur.execute("DELETE FROM bloques_predio_temp;")
    conn.commit()
    cur.execute("DELETE FROM desc_edif_bloque_temp;")
    conn.commit()

    cur.close()
    conn.close()

    return json.dumps({
        "success":'ok'
    })



def upload_file_data(file):   
    conn = connectionDB()
    cur = conn.cursor()
    df = pd.read_excel(file)
    df = pd.DataFrame(df)

    for i in range(len(df['CODIGO'])):
        sql = "UPDATE desc_edificacion_temp SET desed_coefurb = "+str(df['COEFICIENTE'][i])+" WHERE desed_codigo = '0"+str(df['CODIGO'][i])   +"';"
        cur.execute(sql)
        conn.commit()
    
    cur.close()
    conn.close()
    
    return json.dumps({
        "success":True
    })

def getValAllDataTemp():
    conn = connectionDB()
    cur = conn.cursor()

    sql = "select p.divpo_codigo, dp.divpo_nombre, count(1) as predios, sum(vp.valpr_superfconstr) as superfconstr, sum(valpr_valedif) as valedif from valoracion_predio vp left outer join predio p on(p.pre_codigocatastral = vp.pre_codigocatastral) left outer join division_politica dp on(dp.divpo_codigo = p.divpo_codigo) where p.pre_tipo = 'Urbano' group by p.divpo_codigo, dp.divpo_nombre order by p.divpo_codigo;"

    cur.execute(sql)
    rows_predio = cur.fetchall()

    divpo_nombre = [row[1] for row in rows_predio]
    predios      = [row[2] for row in rows_predio]
    superfconstr = [row[3] for row in rows_predio]
    valedif      = [row[4] for row in rows_predio]


    dic_divpo_nombre     = {
        "divpo_nombre"    : [str(divpo_nombre[i]) for i in range(len(divpo_nombre))]
    }
    dic_predios = {"predios": [str(predios[i]) for i in range(len(predios))]}
    dic_superfconstr     = {
        "superfconstr"    : [str(superfconstr[i]) for i in range(len(superfconstr))]
    }
    dic_valedif          = {
        "valedif"         : [str(valedif[i]) for i in range(len(valedif))]
    }
    dic_sum_predios      = {
        "sum_predios"     : str(sum(predios))
    }
    dic_sum_superfconstr = {
        "sum_superfconstr": str(sum(superfconstr))
    }
    dic_sum_valedif      = {
        "sum_valedif"     : str(sum(valedif))
    }

    json_data = json.dumps(
        (
            dic_divpo_nombre,
            dic_predios,
            dic_superfconstr,
            dic_valedif,
            dic_sum_predios,
            dic_sum_superfconstr,
            dic_sum_valedif,
        ),
        indent=4,
    )

    cur.close()
    conn.close()

    return json_data    



