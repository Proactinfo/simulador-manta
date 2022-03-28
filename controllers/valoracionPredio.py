import json
from database.config import connectionDB

def ValoracionPredio(condicion, pisau_codigo):
    conn = connectionDB()
    cur = conn.cursor()

    if pisau_codigo > 0:
        if condicion == None:
            condicion = ""
        else:
            condicion = "and p.pre_codigocatastral = '" + condicion + "'"
        sql_predio = (
            "select p.pre_codigocatastral, p.pre_tipo from predio p where p.pre_estado = 'A' "
            + condicion
            + " order by p.pre_codigocatastral"
        )

        cur.execute(sql_predio)
        rows_predio = cur.fetchall()
        conn.commit()
        for row in rows_predio:
            sql_EB = (
                "select bp.pre_codigocatastral, bp.blopr_numero, bp.blopr_numpiso, bp.blopr_superfconstr, bp.blopr_enconstruccion,(select sum(blopr_numpisos) from bloques_predio where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_enconstruccion = 'NO') as blopr_numpisos,(extract(year from current_timestamp) - bp.blopr_anioconstruccion) as edadconstr, bp.blopr_edadreparacion, vae.valape_codigo,(select valape_item from valor_aplic_edif_item where desed_codigo in(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and desed_codigo like '0201%' order by desed_codigo limit 1)) as matprin,vae.valape_hormigon, vae.valape_hierro, vae.valape_maderafina, vae.valape_maderacomun, vae.valape_bloqueladrillo,vae.valape_bahareque, vae.valape_adobetapial, bp.blopr_porcentajereparacion,(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and substr(desed_codigo, 1, 4) = '0103') as estcon,vae.valape_estable, vae.valape_areparar, vae.valape_obsoleto, (select desed_coefurb from desc_edificacion where desed_codigo = '010501'),(select desed_coefurb from desc_edificacion where desed_codigo = '010502') from bloques_predio bp left outer join valor_aplic_edificacion vae on((case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) >= CAST(coalesce(substr(valape_codigo,0 , (position('-' in valape_codigo))), '0') AS integer) and (case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) <= CAST(coalesce(substr(valape_codigo,(position('-' in valape_codigo)+1)), '0') AS integer)) where bp.pre_codigocatastral = '"
                + row[0]
                + "' and bp.blopr_enconstruccion = 'NO' order by bp.blopr_numero, bp.blopr_numpiso;"
            )

            cur.execute(sql_EB)
            rows_EB = cur.fetchall()
            conn.commit()
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
                Vm2Edif = round(Vm2Rep * FDep * FECon, 4)
                ValorEdif = round(Vm2Edif * SuperfConstr, 2)
             
                sql_UP = (
                    "UPDATE bloques_predio SET blopr_sumatindic = "
                    + str(FDescEdif)
                    + ","
                    + " blopr_valm2reps = "
                    + str(Vm2Rep)
                    + ","
                    + " blopr_valcomerm2 = "
                    + str(Vm2Edif)
                    + ","
                    + " blopr_valcomeredifblo = "
                    + str(ValorEdif)
                    + ","
                    + " pisau_codigo = "
                    + str(pisau_codigo)
                    + " WHERE pre_codigocatastral = '"
                    + str(pre_codigocatastral)
                    + "'"
                    + " AND blopr_numero = "
                    + str(blopr_numero)
                    + " AND blopr_numpiso = "
                    + str(blopr_numpiso)
                    + ";"
                )
                cur.execute(sql_UP)
                conn.commit()
        cur.close()
        conn.close()

        return True


def valoracionPrediosUrb():
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



def valoracionPredioTotal():

    conn = connectionDB()
    cur = conn.cursor()

    sql = "select pre_codigocatastral, pre_tipo from predio where pre_estado = 'A' AND pre_codigocatastral LIKE '1308%'  order by pre_propiedadhorizontal DESC, pre_codigocatastral DESC, pre_tipo DESC;"

    cur.execute(sql)
    rows_predio = cur.fetchall()
    conn.commit()
    for row in rows_predio:
        sql_EB = (
            "select bp.pre_codigocatastral, bp.blopr_numero, bp.blopr_numpiso, bp.blopr_superfconstr, bp.blopr_enconstruccion,(select sum(blopr_numpisos) from bloques_predio where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_enconstruccion = 'NO') as blopr_numpisos,(extract(year from current_timestamp) - bp.blopr_anioconstruccion) as edadconstr, bp.blopr_edadreparacion, vae.valape_codigo,(select valape_item from valor_aplic_edif_item where desed_codigo in(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and desed_codigo like '0201%' order by desed_codigo limit 1)) as matprin,vae.valape_hormigon, vae.valape_hierro, vae.valape_maderafina, vae.valape_maderacomun, vae.valape_bloqueladrillo,vae.valape_bahareque, vae.valape_adobetapial, bp.blopr_porcentajereparacion,(select desed_codigo from desc_edif_bloque where pre_codigocatastral = bp.pre_codigocatastral and blopr_numero = bp.blopr_numero and blopr_numpiso = bp.blopr_numpiso and substr(desed_codigo, 1, 4) = '0103') as estcon,vae.valape_estable, vae.valape_areparar, vae.valape_obsoleto, (select desed_coefurb from desc_edificacion where desed_codigo = '010501'),(select desed_coefurb from desc_edificacion where desed_codigo = '010502') from bloques_predio bp left outer join valor_aplic_edificacion vae on((case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) >= CAST(coalesce(substr(valape_codigo,0 , (position('-' in valape_codigo))), '0') AS integer) and (case when bp.blopr_edadreparacion != 0 then bp.blopr_edadreparacion else (extract(year from current_timestamp) - bp.blopr_anioconstruccion) end) <= CAST(coalesce(substr(valape_codigo,(position('-' in valape_codigo)+1)), '0') AS integer)) where bp.pre_codigocatastral = '"
            + row[0]
            + "' and bp.blopr_enconstruccion = 'NO' order by bp.blopr_numero, bp.blopr_numpiso;"
        )
        cur.execute(sql_EB)
        rows_EB = cur.fetchall()
        conn.commit()
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
                    "WITH DEB AS (select deb.pre_codigocatastral, de.desed_codigopadre, avg(desed_coefurb) as promedio from desc_edif_bloque deb left outer join desc_edificacion de on(de.desed_codigo = deb.desed_codigo) where de.desed_estado = 'A' and deb.pre_codigocatastral = '"
                    + pre_codigocatastral
                    + "' and deb.blopr_numero = "
                    + str(blopr_numero)
                    + " and deb.blopr_numpiso = "
                    + str(blopr_numpiso)
                    + " group by deb.pre_codigocatastral, de.desed_codigopadre) select pre_codigocatastral, sum(deb.promedio) as sumaindicadores from DEB group by pre_codigocatastral;"
                )

            cur.execute(sql_DE)
            rows_DE = cur.fetchall()
            conn.commit()
            for row in rows_DE:
                FDescEdif = (0, round(row[1], 4))[row[1] != None]

            Vm2Rep    = round(KRep * FDescEdif, 4)
            Vm2Edif   = round(Vm2Rep * FDep * FECon, 4)
            ValorEdif = round(Vm2Edif * SuperfConstr, 2)

            sql_UP = (
                    "UPDATE bloques_predio SET blopr_sumatindic = "
                    + str(FDescEdif)
                    + ","
                    + " blopr_valm2reps = "
                    + str(Vm2Rep)
                    + ","
                    + " blopr_valcomerm2 = "
                    + str(Vm2Edif)
                    + ","
                    + " blopr_valcomeredifblo = "
                    + str(ValorEdif)
                    + ","
                    + " pisau_codigo = "
                    + str(7)
                    + " WHERE pre_codigocatastral = '"
                    + str(pre_codigocatastral)
                    + "'"
                    + " AND blopr_numero = "
                    + str(blopr_numero)
                    + " AND blopr_numpiso = "
                    + str(blopr_numpiso)
                    + ";"
                )
            cur.execute(sql_UP)
            conn.commit()
    cur.close()
    conn.close()
    return 'ok'
