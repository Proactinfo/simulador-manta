import json
from database.config import connectionDB
# 13080402030250080000
# 2-03-25-08-000
# 2032508000
def getValoracionPredioByClaveCata(condicion):
    
    conn = connectionDB()
    cur = conn.cursor()

    sql_predio = "SELECT getClaveCata('"+condicion+"');"

    cur.execute(sql_predio)
    rows_predio = cur.fetchall()
    conn.commit()
    if rows_predio != []:
        temp_pre_codigocatastral =[]
        temp_blopr_numero =[]
        temp_blopr_numpiso =[]
        temp_SuperfConstr =[]
        temp_Vm2Rep =[]
        temp_Vm2Rep_tooltips =[]
        temp_Vm2Edif =[]
        temp_Vm2Edif_tooltips =[]
        temp_ValorEdif =[]
        Vm2Rep_tooltipsf=""
        Vm2Edif_tooltipsf=""
        for row in rows_predio:
            sql_EB = (
                "select bp.pre_codigocatastral, bp.blopr_numero, bp.blopr_numpiso, bp.blopr_superfconstr, bp.blopr_enconstruccion,(select sum(blopr_numpisos) from bloques_predio where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_enconstruccion = 'NO') as blopr_numpisos,(extract(year from current_timestamp) - bp.blopr_anioconstruccion) as edadconstr, bp.blopr_edadreparacion, vae.valape_codigo,(select valape_item from valor_aplic_edif_item where desed_codigo in(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and desed_codigo like '0201%' order by desed_codigo limit 1)) as matprin,vae.valape_hormigon, vae.valape_hierro, vae.valape_maderafina, vae.valape_maderacomun, vae.valape_bloqueladrillo,vae.valape_bahareque, vae.valape_adobetapial, bp.blopr_porcentajereparacion,(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and substr(desed_codigo, 1, 4) = '0103') as estcon,vae.valape_estable, vae.valape_areparar, vae.valape_obsoleto, (select desed_coefurb from desc_edificacion where desed_codigo = '010501'),(select desed_coefurb from desc_edificacion where desed_codigo = '010502') from bloques_predio bp left outer join valor_aplic_edificacion vae on((case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) >= CAST(coalesce(substr(valape_codigo,0 , (position('-' in valape_codigo))), '0') AS integer) and (case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) <= CAST(coalesce(substr(valape_codigo,(position('-' in valape_codigo)+1)), '0') AS integer)) where bp.pre_codigocatastral = '"
                + row[0]
                + "' and bp.blopr_enconstruccion = 'NO' order by bp.blopr_numero, bp.blopr_numpiso;"
            )

            cur.execute(sql_EB)
            rows_EB = cur.fetchall()
            conn.commit()
            if rows_EB != []:
                for row in rows_EB:
                    pre_codigocatastral = row[0]
                    blopr_numero = row[1]
                    blopr_numpiso = row[2]
                    SuperfConstr = (0, row[3])[row[3] != None]
                    NumPisos = row[5]
                    MatPrin = ("", row[9])[row[9] != None]
                    PorDep = (0, row[17])[row[17] != None]
                    EstCon = ("", row[18])[row[18] != None]
                    # FACTOR DEPRECIACION
                    if MatPrin == "valape_hormigon":
                        FDep = (0, row[10])[row[10] != None]
                    elif MatPrin == "valape_hierro":
                        FDep = (0, row[11])[row[11] != None]
                    elif MatPrin == "valape_maderafina":
                        FDep = (0, row[12])[row[12] != None]
                    elif MatPrin == "valape_maderacomun":
                        FDep = (0, row[13])[row[13] != None]
                    elif MatPrin == "valape_bloqueladrillo":
                        FDep = (0, row[14])[row[14] != None]
                    elif MatPrin == "valape_bahareque":
                        FDep = (0, row[15])[row[15] != None]
                    elif MatPrin == "valape_adobetapial":
                        FDep = (0, row[16])[row[16] != None]
                    else:
                        FDep = 1

                    # ESTADO DE CONSERVACION
                    if PorDep > 0:
                        FECon = round((100 - PorDep) / 100, 4)
                    else:
                        if EstCon == "010301" or EstCon == "010302":
                            FECon = (0, row[19])[row[19] != None]
                        elif EstCon == "010303" or EstCon == "010304":
                            FECon = (0, row[20])[row[20] != None]
                        elif EstCon == "010305":
                            FECon = (0, row[21])[row[21] != None]
                        else:
                            FECon = (0, row[19])[row[19] != None]

                    # CONST REPOSICION

                    KRep = row[22]

                    if NumPisos > 1:
                        KRep = row[23]

                    FDescEdif = 0

                    sql_DE = (
                        "WITH DEB AS (select deb.pre_codigocatastral, de.desed_codigopadre, avg(desed_coefurb) as promedio from desc_edif_bloque deb left outer     join desc_edificacion de on(de.desed_codigo = deb.desed_codigo) where de.desed_estado = 'A' and deb.pre_codigocatastral = '"
                        + pre_codigocatastral
                        + "' and deb.blopr_numero = "
                        + str(blopr_numero)
                        + " and deb.blopr_numpiso = "
                        + str(blopr_numpiso)
                        + " group by deb.pre_codigocatastral, de.    desed_codigopadre) select pre_codigocatastral, sum(deb.promedio) as sumaindicadores from DEB group by pre_codigocatastral;"
                    )

                    cur.execute(sql_DE)
                    rows_DE = cur.fetchall()
                    conn.commit()
                    for row in rows_DE:
                        FDescEdif = (0, round(row[1], 4))[row[1] != None]

                    Vm2Rep = round(KRep * FDescEdif, 4)
                    Vm2Rep_tooltipsf = "KRep*FDescEdif"
                    Vm2Rep_tooltips = str(round(KRep,2))+"*"+str(round(FDescEdif,2))
                    Vm2Edif = round(Vm2Rep * FDep * FECon, 4)
                    Vm2Edif_tooltipsf = "Vm2Rep*FDep*FECon"
                    Vm2Edif_tooltips= str(round(Vm2Rep,2))+"*"+str(round(FDep,2))+"*"+str(round(FECon,2))
                    ValorEdif = round(Vm2Edif * SuperfConstr, 2)


                    temp_pre_codigocatastral.append(pre_codigocatastral)
                    temp_blopr_numero.append(blopr_numero)
                    temp_blopr_numpiso.append(blopr_numpiso)
                    temp_SuperfConstr.append(SuperfConstr)
                    temp_Vm2Rep.append(Vm2Rep)
                    temp_Vm2Rep_tooltips.append(Vm2Rep_tooltips)
                    temp_Vm2Edif.append(Vm2Edif)
                    temp_Vm2Edif_tooltips.append(Vm2Edif_tooltips)
                    temp_ValorEdif.append(ValorEdif)

                dic_temp_pre_codigocatastral  = { "pre_codigocatastral" :  temp_pre_codigocatastral[0]                                                  }
                dic_temp_blopr_numero         = { "blopr_numero"        : [str(temp_blopr_numero[i] )     for i in range(len( temp_blopr_numero ))]     }
                dic_temp_blopr_numpiso        = { "blopr_numpiso"       : [str(temp_blopr_numpiso[i])     for i in range(len( temp_blopr_numpiso ))]    }
                dic_temp_SuperfConstr         = { "blopr_superfconstr"  : [str(temp_SuperfConstr[i] )     for i in range(len( temp_SuperfConstr ))]     }
                dic_temp_SuperfConstrTotal    = { "SuperfConstrTotal"   :  str(sum(temp_SuperfConstr))                                                  }
                dic_temp_Vm2Rep               = { "Vm2Rep"              : [str(temp_Vm2Rep[i])            for i in range(len( temp_Vm2Rep ))]           }
                dic_temp_Vm2Rep_tooltips      = { "Vm2Rep_tooltips"     : [str(temp_Vm2Rep_tooltips[i])   for i in range(len( temp_Vm2Rep_tooltips ))]  }
                dic_temp_Vm2Rep_tooltipsf     = { "Vm2Rep_tooltipsf"    :  Vm2Rep_tooltipsf                                                             }
                dic_temp_Vm2Edif              = { "Vm2Edif"             : [str(temp_Vm2Edif[i])           for i in range(len( temp_Vm2Edif ))]          }
                dic_temp_Vm2Edif_tooltips     = { "Vm2Edif_tooltips"    : [str(temp_Vm2Edif_tooltips[i])  for i in range(len( temp_Vm2Edif_tooltips ))] }
                dic_temp_Vm2Edif_tooltipsf    = { "Vm2Edif_tooltipsf"   :  Vm2Edif_tooltipsf                                                            }
                dic_temp_ValorEdif            = { "ValorEdif"           : [str(temp_ValorEdif[i])         for i in range(len( temp_ValorEdif ))]        } 
                dic_temp_Total                = { "Total"               :  str(sum(temp_ValorEdif))                                                     } 
            else:
                return json.dumps((
                    [{"pre_codigocatastral":rows_predio[0][0]},
                        {"blopr_numero"       : [0] },
                        {"blopr_numpiso"      : [0] },
                        {"blopr_superfconstr" : [0] },
                        {"SuperfConstrTotal"  :  0  },
                        {"Vm2Rep"             :  0  },
                        {"Vm2Rep_tooltips"    :  0  },
                        {"Vm2Rep_tooltipsf"   : [0] },
                        {"Vm2Edif"            : [0] },
                        {"Vm2Edif_tooltips"   : [0] },
                        {"Vm2Edif_tooltipsf"  :  0  },
                        {"ValorEdif"          : [0] },
                        {"Total"              :  0  }]

                ),indent=4)
        cur.close()
        conn.close()


        return json.dumps((
        dic_temp_pre_codigocatastral,
        dic_temp_blopr_numero,
        dic_temp_blopr_numpiso,
        dic_temp_SuperfConstr,
        dic_temp_SuperfConstrTotal,
        dic_temp_Vm2Rep,
        dic_temp_Vm2Rep_tooltips,
        dic_temp_Vm2Edif,
        dic_temp_Vm2Edif_tooltips,
        dic_temp_ValorEdif,
        dic_temp_Total,
        dic_temp_Vm2Rep_tooltipsf,
        dic_temp_Vm2Edif_tooltipsf            
        ),indent=4)            
    else:
        return json.dumps(([{"pre_codigocatastral":None}]),indent=4)

def getDataEdifByClaveCata(claveCata):

    conn = connectionDB()
    cur = conn.cursor()

    if claveCata == None:
        return json.dumps({
            "messaje":"ingrese clave catastral"
        })


    
    sql_query_claveCata = "SELECT getClaveCata('"+claveCata+"');"
    cur.execute(sql_query_claveCata)
    row_sql_query_claveCata = cur.fetchall()
    conn.commit()

    sql_cur = "select bp.pre_codigocatastral,bp.blopr_numero,bp.blopr_numpiso from bloques_predio bp where bp.pre_codigocatastral = '" +row_sql_query_claveCata[0][0]+"' order by bp.blopr_numero,blopr_numpiso;"

    cur.execute(sql_cur)
    row_sq_cur = cur.fetchall()
    conn.commit()

    if row_sq_cur != []:
        pre_codigocatastra = [ ]
        blopr_num      = [ ]
        blopr_numpiso      = [ ]
        desed_codigo       = [ ]
        desed_descri       = [ ]
        
        for row in row_sq_cur:
            sql= "SELECT deb.desed_codigo, de.desed_descripcion FROM desc_edif_bloque deb LEFT JOIN desc_edificacion de on (deb.desed_codigo =de.desed_codigo) WHERE deb.pre_codigocatastral = '" + row[0] + "' AND  deb.blopr_numero = " + str(row[1]) + " AND  deb.blopr_numpiso = " + str(row[2])+ " AND  de.desed_estado = 'A' AND (deb.desed_codigo LIKE '02%'    OR deb.desed_codigo LIKE  '03%' OR deb.desed_codigo LIKE '04%' ) ORDER BY deb.desed_codigo;"



            cur.execute(sql)
            sql_data = cur.fetchall()

                        
            pre_codigocatastra.append(row[0])
            blopr_num.append(row[1])
            blopr_numpiso.append(row[2])
            desed_codigo_data = [rows[0]  for rows in sql_data] 
            desed_descri_data = [rows[1]  for rows in sql_data] 
            desed_codigo.append( desed_codigo_data ) 
            desed_descri.append( desed_descri_data ) 


            conn.commit()

        dict_pre_codigocatastra = {"pre_codigocatastra": str(pre_codigocatastra[0]) }
        dict_blopr_num          = {"blopr_num"         : blopr_num }
        dict_blopr_numpiso      = {"blopr_numpiso"     : blopr_numpiso }
        dict_desed_codigo       = {"desed_codigo"      : desed_codigo}
        dict_desed_descri       = {"desed_descri"      : desed_descri}
        

        return json.dumps((dict_pre_codigocatastra,
                           dict_blopr_num,
                           dict_blopr_numpiso,
                           dict_desed_codigo,
                           dict_desed_descri),indent=4)
    else:
        return json.dumps({
            "message":"Clave Catastral no disposible"
        })

