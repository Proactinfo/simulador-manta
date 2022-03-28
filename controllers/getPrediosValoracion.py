import json
from database.config import connectionDB



def getEdif():
    conn = connectionDB()
    cur = conn.cursor()

    sql_cur = "SELECT desed_codigo, desed_codigopadre, desed_descripcion FROM desc_edificacion WHERE desed_estado = 'A' AND (desed_codigo LIKE '02%' OR desed_codigo LIKE '03%' OR desed_codigo LIKE '04%') ORDER BY desed_codigo;"
    
    cur.execute(sql_cur)

    row_cur = cur.fetchall()

    desed_codigo           = [ row[0] for row in row_cur ]
    desed_codigopadre      = [ row[1] for row in row_cur ]
    desed_descripcion      = [ row[2] for row in row_cur ]

    dic_desed_codigo       = { "desed_codigo"       : [str(desed_codigo[i])         for i in range(len( desed_codigo ))] }
    dic_desed_codigopadre  = { "desed_codigopadre"  : [str(desed_codigopadre[i])    for i in range(len( desed_codigopadre ))]  }
    dic_desed_descripcion  = { "desed_descripcion"  : [str(desed_descripcion[i])    for i in range(len( desed_descripcion ))]  }


    cur.close()
    conn.close()

    return json.dumps((dic_desed_codigo,
                            dic_desed_codigopadre,
                            dic_desed_descripcion), indent=4)


def getEdifPredioCod(claveCata):

    conn = connectionDB()
    cur = conn.cursor()
    
    sql_cur = "select bp.pre_codigocatastral,bp.blopr_numero,bp.blopr_numpiso from bloques_predio bp where bp.pre_codigocatastral = '" +claveCata+"' order by bp.blopr_numero,blopr_numpiso;"

    cur.execute(sql_cur)

    data_sql_cur = cur.fetchall()
    conn.commit()
    pre_codigocatastral = []
    blopr_numero        = []
    blopr_numpiso       = []
    desed_codigo        = []
  
    for row in data_sql_cur:
        sql_cur_bloq = "SELECT desed_codigo FROM desc_edif_bloque WHERE pre_codigocatastral = '" + row[0] + "' AND blopr_numero = " + str(row[1]) + " AND blopr_numpiso = " + str(row[2])+ " AND desed_codigo IN(SELECT desed_codigo FROM desc_edificacion WHERE desed_estado = 'A') AND (desed_codigo LIKE '02%' OR desed_codigo LIKE '03%' OR desed_codigo LIKE '04%') ORDER BY desed_codigo;"
        
        cur.execute(sql_cur_bloq)

        data_sql_cur_bloq = cur.fetchall()
        conn.commit()
        pre_codigocatastral.append(row[0])
        blopr_numero.append(row[1]) 
        blopr_numpiso.append(row[2])
        desed_codigo_data = [ rows[0] for rows in data_sql_cur_bloq]
        desed_codigo.append(desed_codigo_data)

    pre_codigocatastral = { 'pre_codigocatastral':[str(pre_codigocatastral[i]) for i in range(len(pre_codigocatastral))] }
    blopr_numero        = { 'blopr_numero':[str(blopr_numero[i]) for i in range(len(blopr_numero))]}
    blopr_numpiso       = { 'blopr_numpiso':[str(blopr_numpiso[i]) for i in range(len(blopr_numpiso))]}
    desed_codigo        = { 'desed_codigo':[desed_codigo[i] for i in range(len(desed_codigo))]}
    

    json_data = json.dumps((pre_codigocatastral,
                            blopr_numero,
                            blopr_numpiso,
                            desed_codigo),indent=4)
    cur.close()
    conn.close()

    return json_data

def getEdifPreBloqPiso(numClaveCata,numBloqCata,numBloqPisoCata,numsBloqPiso,numDesedCodigo,condicion):
    conn = connectionDB()
    cur = conn.cursor()
    
    if condicion == None:
        condicion = ''

    for i in numsBloqPiso:

        if i[1]=='-':
            sql_delete ="DELETE FROM desc_edif_bloque  WHERE pre_codigocatastral = '" + numClaveCata + "'  AND blopr_numero = " + i[0]+ " AND blopr_numpiso = " + i[2:] +" AND desed_codigo LIKE '"+condicion+"%';"
            cur.execute(sql_delete)
            conn.commit()

        elif i[2] =='-':
            print(i[0:1],'-',i[3:])
            sql_delete ="DELETE FROM desc_edif_bloque  WHERE pre_codigocatastral = '" + numClaveCata + "'  AND blopr_numero = " + i[0]+ " AND blopr_numpiso = " + i[2:] +"AND  desed_codigo LIKE '"+condicion+"%';"
            cur.execute(sql_delete)
            conn.commit()

    for i in range(len(numBloqCata)):  
        sql_insert = "INSERT INTO desc_edif_bloque (pre_codigocatastral, blopr_numero, blopr_numpiso, desed_codigo) VALUES('" + numClaveCata + "', " + numBloqCata[i] + "," + numBloqPisoCata[i] + ",'" + numDesedCodigo[i] + "');"
        cur.execute(sql_insert)
        conn.commit()

    cur.close()
    conn.close()

    return 'ok'
    








