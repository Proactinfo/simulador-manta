import os
from database.config import connectionDB
import json

PATH_O = os.getcwd()
PATH = os.getcwd()+"/static/predios"

def getPhotosByClaveCata(claveCata):

    conn = connectionDB()
    counter = 0
    os.chdir(PATH)

    cur = conn.cursor()
    print(os.getcwd())

    sql_query_claveCata = "SELECT getClaveCata('"+claveCata+"');"
    cur.execute(sql_query_claveCata)
    row_sql_query_claveCata = cur.fetchall()
    conn.commit()
    print(row_sql_query_claveCata)
    sql_query_cod = "SELECT preim_codigo, pre_codigocatastral, preim_descripcion, preim_fecha, preim_principal, preim_coordenadax, preim_coordenaday  FROM predio_imagen  WHERE pre_codigocatastral = '"+row_sql_query_claveCata[0][0]+"' ORDER BY preim_fecha DESC, preim_codigo DESC;"
    
    cur.execute(sql_query_cod)
    row_sql_query_cod = cur.fetchall()
    conn.commit()
    
    claveCata_sql= []

    if row_sql_query_cod != []:
        for row in row_sql_query_cod:
            sql_query_photo_pre = "SELECT preim_imagen , pre_codigocatastral FROM predio_imagen WHERE preim_codigo = "+str(row[0])+";"
            cur.execute(sql_query_photo_pre)
            photo_predios_cod = cur.fetchall()

            conn.commit()

            for rows in photo_predios_cod:
                claveCata_sql.append(row[1])

                with open("{}.jpg".format(rows[1]+"-"+str(counter)),"wb") as f:
                    f.write(rows[0])
                    counter= counter + 1
        os.chdir(PATH_O)
        print(os.getcwd())
    else:
        os.chdir(PATH_O)
        return json.dumps({
        "claveCatastral":claveCata,
        "count":0
        })

    cur.close()
    conn.close()
    os.chdir(PATH_O)
    return json.dumps({
        "claveCatastral":claveCata_sql[0],
        "count":counter
    })