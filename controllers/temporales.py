import json
from database.config import connectionDB

import psycopg2



def valoracionTempByClaveCata(claveCata):
    
    conn = connectionDB()
    cur  = conn.cursor()
    if claveCata == None or  claveCata == "":
        return json.dumps({"message":"Ingrese clave catastral"})
    else : 
        queryClaveCata = "call valPreUrbTemp('"+claveCata+"');"
        cur.execute(queryClaveCata)
        
        
        # print(conn.notices[0][0])
        conn.commit()
        
        cur.close()
        conn.close()
        return json.dumps({"message":"ok"})




def setEdifBpTempByClaveCata(numClaveCata,numBloqCata,numBloqPisoCata,numDesedCodigo):
    
    conn = connectionDB()
    cur = conn.cursor()

    sql_delete ="DELETE FROM desc_edif_bloque_temp deb WHERE deb.pre_codigocatastral = '" + numClaveCata + "' AND (deb.desed_codigo LIKE '02%' OR deb.desed_codigo LIKE '03%' OR deb.desed_codigo LIKE '04%');"
    cur.execute(sql_delete)
    conn.commit()

    for i in range(len(numBloqCata)):  
        sql_insert = "INSERT INTO desc_edif_bloque_temp (pre_codigocatastral, blopr_numero, blopr_numpiso, desed_codigo) VALUES('" + numClaveCata + "', " + numBloqCata[i] + "," + numBloqPisoCata[i] + ",'" + numDesedCodigo[i] + "');"
        cur.execute(sql_insert)
        conn.commit()

    cur.close()
    conn.close()

    return json.dumps({"message":"ok"})

# uploadBloqByClaveCata
def setDataBloqPisoByClaveCata(claveCata):

    conn = connectionDB()
    cur = conn.cursor()
    sql = "select bp.pre_codigocatastral ,bp.blopr_numero,bp.blopr_numpiso,bp.blopr_superfconstr,bp.blopr_anioconstruccion,( select deb.desed_codigo from desc_edif_bloque deb where deb.pre_codigocatastral = bp.pre_codigocatastral and deb.desed_codigo like '0103%' order by deb.desed_codigo limit 1 ) from bloques_predio bp where bp.pre_codigocatastral = '"+claveCata+"' order by bp.blopr_numero,bp.blopr_numpiso;"

    cur.execute(sql)
    row = cur.fetchall()
    pre_codigocatastral = []
    blopr_num  = []
    blopr_numpiso = []
    blopr_superfconstr = []
    blopr_anioconstruccion = []
    desed_codigo = []
    
    if row != []:
        pre_codigocatastral.append(row[0][0])
        for i in row:
            blopr_num.append(i[1])
            blopr_numpiso.append(i[2])
            blopr_superfconstr.append(str(i[3]))
            blopr_anioconstruccion.append(i[4])
            desed_codigo.append(i[5])

        dic_pre_codigocatastral     =  {"pre_codigocatastral": pre_codigocatastral}
        dic_blopr_num               =  {"blopr_num": blopr_num}
        dic_blopr_numpiso           =  {"blopr_numpiso": blopr_numpiso}
        dic_blopr_superfconstr      =  {"blopr_superfconstr": blopr_superfconstr}
        dic_blopr_anioconstruccion  =  {"blopr_anioconstruccion": blopr_anioconstruccion}
        dic_desed_codigo            =  {"desed_codigo": desed_codigo}
        return json.dumps((dic_pre_codigocatastral,
                           dic_blopr_num,
                           dic_blopr_numpiso,
                           dic_blopr_superfconstr,
                           dic_blopr_anioconstruccion,
                           dic_desed_codigo),indent=4)
            
    else:
         return json.dumps({"message":"no se encontro informacion sobre ese predio"})


def setUpdateDataBloquesByClaveCata(pre_codigocatastral,bloq_num,bloq_piso,blopr_superfconstr,blopr_anioconstruccion,desed_codigo):

    conn = connectionDB()
    cur  = conn.cursor()

    
    if pre_codigocatastral == None or pre_codigocatastral == "":
        return json.dumps({"msg":"Ingrese Clave Catastral"})
    else:

        for i in range(len(bloq_num)):
            cur.execute('CALL upDataBpByClaveCata(%s,%s,%s,%s,%s,%s);',(str(pre_codigocatastral),int(bloq_num[i]),int(bloq_piso[i]),float(blopr_superfconstr[i]),int(blopr_anioconstruccion[i]),str(desed_codigo[i])))
            conn.commit()

        cur.close()
        conn.close()

        return json.dumps({"message":"ok"})











def getValTempByCalveCata(claveCata):

    conn = connectionDB()
    cur = conn.cursor()

    if claveCata == None:
        claveCata = ''

    sql_cur = "select bp.pre_codigocatastral,bp.blopr_numero,bp.blopr_numpiso,bp.blopr_superfconstr,bp.blopr_valcomerm2,bp.blopr_valcomeredifblo,bp.blopr_anioconstruccion,(select de.desed_descripcion from desc_edif_bloque_temp deb left join desc_edificacion_temp de on de.desed_codigo = deb.desed_codigo where deb.pre_codigocatastral = bp.pre_codigocatastral and deb.blopr_numero = bp.blopr_numero and deb.blopr_numpiso = bp.blopr_numpiso and deb.desed_codigo like '0103%' ) as estado,(select sum(bp.blopr_valcomeredifblo) from bloques_predio_temp bp where bp.pre_codigocatastral = '"+claveCata+"' ) as total from bloques_predio_temp bp where bp.pre_codigocatastral = '"+claveCata+"' order by pre_codigocatastral,blopr_numero,blopr_numpiso;"
    
    cur.execute(sql_cur)

    row_cur = cur.fetchall()
    pre_codigocatastral     = [ row[0] for row in row_cur ]
    blopr_numero            = [ row[1] for row in row_cur ]
    blopr_numpiso           = [ row[2] for row in row_cur ]
    blopr_superfconstr      = [ row[3] for row in row_cur ]
    blopr_valcomerm2        = [ row[4] for row in row_cur ]
    blopr_valcomeredifblo   = [ row[5] for row in row_cur ]
    blopr_anioconstruccion  = [ row[6] for row in row_cur ]
    estado                  = [ row[7] for row in row_cur ]
    Total                   = [ row[8] for row in row_cur ]
    sum_superfconstr = sum(blopr_superfconstr)
 
    dic_pre_codigocatastral    = { "pre_codigocatastral"     : pre_codigocatastral[0] }
    dic_blopr_numero           = { "blopr_numero"            : [str(blopr_numero[i])           for i in range(len( blopr_numero ))]  }
    dic_blopr_numpiso          = { "blopr_numpiso"           : [str(blopr_numpiso[i])          for i in range(len( blopr_numpiso ))]  }
    dic_blopr_superfconstr     = { "blopr_superfconstr"      : [str(blopr_superfconstr[i])     for i in range(len( blopr_superfconstr ))]  }
    dic_blopr_valcomerm2       = { "blopr_valcomerm2"        : [str(blopr_valcomerm2[i])       for i in range(len( blopr_valcomerm2 ))]  }
    dic_blopr_valcomeredifblo  = { "blopr_valcomeredifblo"   : [str(blopr_valcomeredifblo[i])  for i in range(len( blopr_valcomeredifblo ))]  }
    dic_blopr_anioconstruccion = { "blopr_anioconstruccion"  : [str(blopr_anioconstruccion[i]) for i in range(len( blopr_anioconstruccion ))]  }
    dic_estado                 = { "estado"                  : [str(estado[i])                 for i in range(len( estado ))]  }
    dic_Total                  = { "Total"                   : str(Total[0]) }
    dic_sum_superfconstr      =  { "sum_superfconstr"        : str(sum_superfconstr) }

    json_data = json.dumps((dic_pre_codigocatastral,
                            dic_blopr_numero,
                            dic_blopr_numpiso,
                            dic_blopr_superfconstr,
                            dic_blopr_valcomerm2,
                            dic_blopr_valcomeredifblo,
                            dic_blopr_anioconstruccion,
                            dic_estado,
                            dic_Total,
                            dic_sum_superfconstr), indent=4)


    cur.close()
    conn.close()

    return json_data


def getValByCalveCata(claveCata):

    conn = connectionDB()
    cur = conn.cursor()

    if claveCata == None:
        claveCata = ''

    sql_cur = "select bp.pre_codigocatastral,bp.blopr_numero,bp.blopr_numpiso,bp.blopr_superfconstr,bp.blopr_valcomerm2,bp.blopr_valcomeredifblo,bp.blopr_anioconstruccion,(select de.desed_descripcion from desc_edif_bloque deb left join desc_edificacion de on de.desed_codigo = deb.desed_codigo where deb.pre_codigocatastral = bp.pre_codigocatastral and deb.blopr_numero = bp.blopr_numero and deb.blopr_numpiso = bp.blopr_numpiso and deb.desed_codigo like '0103%' ) as estado,(select sum(bp.blopr_valcomeredifblo) from bloques_predio bp where bp.pre_codigocatastral = '"+claveCata+"' ) as total from bloques_predio bp where bp.pre_codigocatastral = '"+claveCata+"' order by pre_codigocatastral;"
    
    cur.execute(sql_cur)

    row_cur = cur.fetchall()
    pre_codigocatastral     = [ row[0] for row in row_cur ]
    blopr_numero            = [ row[1] for row in row_cur ]
    blopr_numpiso           = [ row[2] for row in row_cur ]
    blopr_superfconstr      = [ row[3] for row in row_cur ]
    blopr_valcomerm2        = [ row[4] for row in row_cur ]
    blopr_valcomeredifblo   = [ row[5] for row in row_cur ]
    blopr_anioconstruccion  = [ row[6] for row in row_cur ]
    estado                  = [ row[7] for row in row_cur ]
    Total                   = [ row[8] for row in row_cur ]
    sum_superfconstr = sum(blopr_superfconstr)
 
    dic_pre_codigocatastral    = { "pre_codigocatastral"     : pre_codigocatastral[0] }
    dic_blopr_numero           = { "blopr_numero"            : [str(blopr_numero[i])           for i in range(len( blopr_numero ))]  }
    dic_blopr_numpiso          = { "blopr_numpiso"           : [str(blopr_numpiso[i])          for i in range(len( blopr_numpiso ))]  }
    dic_blopr_superfconstr     = { "blopr_superfconstr"      : [str(blopr_superfconstr[i])     for i in range(len( blopr_superfconstr ))]  }
    dic_blopr_valcomerm2       = { "blopr_valcomerm2"        : [str(blopr_valcomerm2[i])       for i in range(len( blopr_valcomerm2 ))]  }
    dic_blopr_valcomeredifblo  = { "blopr_valcomeredifblo"   : [str(blopr_valcomeredifblo[i])  for i in range(len( blopr_valcomeredifblo ))]  }
    dic_blopr_anioconstruccion = { "blopr_anioconstruccion"  : [str(blopr_anioconstruccion[i]) for i in range(len( blopr_anioconstruccion ))]  }
    dic_estado                 = { "estado"                  : [str(estado[i])                 for i in range(len( estado ))]  }
    dic_Total                  = { "Total"                   : str(Total[0]) }
    dic_sum_superfconstr      =  { "sum_superfconstr"        : str(sum_superfconstr) }

    json_data = json.dumps((dic_pre_codigocatastral,
                            dic_blopr_numero,
                            dic_blopr_numpiso,
                            dic_blopr_superfconstr,
                            dic_blopr_valcomerm2,
                            dic_blopr_valcomeredifblo,
                            dic_blopr_anioconstruccion,
                            dic_estado,
                            dic_Total,
                            dic_sum_superfconstr), indent=4)


    cur.close()
    conn.close()

    return json_data


def getValByCalveCataManta(claveCata):

    conn = connectionDB()
    cur = conn.cursor()

    sql = (
        "select  blopr_numero, blopr_numpiso, blopr_areacomunal, blopr_superfconstr, blopr_valorindividual, blopr_valorcomunal  from bloques_predio bp where bp.pre_codigocatastral ='"
        + claveCata
        + "'order by blopr_numero,blopr_numpiso"
    )
    cur.execute(sql)
    rows_predio = cur.fetchall()

    blopr_numero = [row[0] for row in rows_predio]
    blopr_numpiso = [row[1] for row in rows_predio]
    blopr_areacomunal = [row[2] for row in rows_predio]
    blopr_superfconstr = [row[3] for row in rows_predio]
    blopr_valorindividual = [row[4] for row in rows_predio]
    blopr_valorcomunal = [row[5] for row in rows_predio]


    dic_blopr_numero = {
        "blopr_numero": [str(blopr_numero[i]) for i in range(len(blopr_numero))]
    }
    dic_blopr_numpiso = {
        "blopr_numpiso": [str(blopr_numpiso[i]) for i in range(len(blopr_numpiso))]
    }
    dic_blopr_areacomunal = {
        "blopr_areacomunal": [
            str(blopr_areacomunal[i]) for i in range(len(blopr_areacomunal))
        ]
    }
    dic_blopr_superfconstr = {
        "blopr_superfconstr": [
            str(blopr_superfconstr[i]) for i in range(len(blopr_superfconstr))
        ]
    }
    dic_blopr_valorindividual = {
        "blopr_valorindividual": [
            str(blopr_valorindividual[i]) for i in range(len(blopr_valorindividual))
        ]
    }
    dic_blopr_valorcomunal = {
        "blopr_valorcomunal": [
            str(blopr_valorcomunal[i]) for i in range(len(blopr_valorcomunal))
        ]
    }
    dic_sum_blopr_areacomunal       = {"sum_blopr_areacomunal"      : str(sum(blopr_areacomunal))    }
    dic_sum_blopr_superfconstr      = {"sum_blopr_superfconstr"     : str(sum(blopr_superfconstr))   }
    dic_sum_blopr_valorindividual   = {"sum_blopr_valorindividual"  : str(sum(blopr_valorindividual))}
    dic_sum_blopr_valorcomunal      = {"sum_blopr_valorcomunal"     : str(sum(blopr_valorcomunal))   }

    json_data = json.dumps(
        (
            dic_blopr_numero,
            dic_blopr_numpiso,
            dic_blopr_areacomunal,
            dic_blopr_superfconstr,
            dic_blopr_valorindividual,
            dic_blopr_valorcomunal,
            dic_sum_blopr_areacomunal,
            dic_sum_blopr_superfconstr,
            dic_sum_blopr_valorindividual,
            dic_sum_blopr_valorcomunal,
        ),
        indent=4,
    )
    cur.close()
    conn.close()

    return json_data


def queryTempDataByClaveCata(claveCata):

    conn = connectionDB()
    cur  = conn.cursor()
    if claveCata == None or  claveCata == "":
        return json.dumps({"message":"Ingrese clave catastral"})
    else : 
        queryClaveCata = "call setclavecatatemp('"+claveCata+"');"
        cur.execute(queryClaveCata)
        conn.commit()
        
        cur.close()
        conn.close()
        return json.dumps({"message":"clave catastral creada en la tabla temporal"})


def getValSueloByPre(ClaveCata):
    conn = connectionDB()
    cur =  conn.cursor()

    sql = "select pre_codigocatastral, pre_valterreno from predio where pre_codigocatastral = '"+ClaveCata+"';"

    cur.execute(sql)

    data_sql = cur.fetchall()
    print(data_sql[0][1])
    return json.dumps({'val_predio':str(data_sql[0][1])})
