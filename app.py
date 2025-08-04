import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import os
import dropbox

# ---------- Configuración Dropbox ----------
# En .streamlit/secrets.toml define:
# [dropbox]
# access_token = "SL.U.TU_TOKEN_GENERADO"

dbx = dropbox.Dropbox(st.secrets["dropbox"]["sl.u.AF55e316r2TRtIsH8iHVLEuiBRRw8g_cY_nBe-0i0kHjR4DfNPgn3qJ4GjVy7PwQYFlt_YnmzWG9wctszI67Htbq81MVHzgyvBQjo5lL41WpWG7Dv4P-vFPnVUxrfMOWPB5wJyyE4CeRVvj36n5jFtJ3Nj-9rCCSfeVdM2VNfODr8t84K4m1E-O695qW2Ha9MUOwwiXidbk1hzhlz40d1NppezoYnEwYGj-Ck74glPsT12rnoGpGXw4Oo4dkXWtmCUYUYixfbZpTTXmVlc4EGIYQHwqPAuVvWn7oE8E3pasqMaa0161c5GkHHQhFH3XD9EDQg7RxtK9NbJi6vRN7qYH8n0-IL9dwMwDmsesiCxvyeAcHCqnboEN3Tm6hzu_Z0ed4Y74irQIC7hOKoF5zMIgIllLkrcDRNXSbjGGP7b2uT31k_j7OeGxpIigKjWOrTsCEeTRHp8oMd9QUXULW_If9y3GdHtKDLal6udwMPe887sbrpCvAA42xk2QaSldJsQbQVd8hKwy8b_wUyM4N9DsW20hiXY5sfRgaTsdKPTJb6lfD5dB7Cd129vNAP_HNt2VQSToV1Ob8vmEQs9yobL4OLQJ726MEEfvQU4VwENbV77EhxBTK-oo_HlOk6_3erfCSxT7o5-W7dswRhTS6lg2fI72rvLael1WMAUFPg7wVq3G9QLtvLvYZQfLmqTmVdJfszA9_5xCrk4AIe0qoXjP6BYfNqHdYphcO1Pxs7Icl5e0NkHOFqpgkwVy-W2cPQkI1hPSgCokd6Id1hUh-uLfp3wkMdQSM7uDpCaZ-wxcTW2tZMY7qBaKWEXsNyCRiveo1Wo6WBrJEm0nBqVZptc7FMdTBEt069U9K80qHZXli0Rqnt9eSnfT59T6ySahthblxHqov14DzJRwNI-p-1b4yRVL8RA2M68_zoPBIRMNYBYUr5zdXI4sFG53XH60uwzFsp0wC6dZbMTzwar6O3-oK3hIEssDQzIwlB2MQeacV_6z-K8KhHp77a4xRe55TbQnnMxkpybv4p6g-0yZgnxXLLkQimHfxZmljts7cV7EDfsQIIS8UkbHLhDTaPaRANp4YVndHFIwS7xAuPfOYwY6ss6z4UPgYUhOa7WhyBFaHbv7buC50wpNpF__9l5Npl3WU5h-hms3WdfyPvnP1XPGqDHk2BdoFwVqIzzO1zGiq7v6XP4g2zkBNDniJbeaOM4Z1r6BdEtsfODwugnglYAo9JCaJb7XThMHitp6JNa4DvOnpKGOfqZEBA76JjMomwNSNMaIuOUP84IHHO2q9YfC5"])

def upload_to_dropbox(data_bytes: bytes, filename: str) -> str:
    dropbox_path = f"/{filename}"
    try:
        dbx.files_upload(data_bytes, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        link_meta = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        return link_meta.url.replace("?dl=0", "?dl=1")
    except dropbox.exceptions.ApiError as e:
        st.error(f"❌ Error subiendo a Dropbox:\n{e}")
        return None

# Inicializamos en sesión las “tablas” en memoria
for key in ("cabeceras", "clientes", "operaciones", "transacciones"):
    if key not in st.session_state:
        st.session_state[key] = []

# Configuración de la página
st.set_page_config(
    page_title='Formulario UAFE',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.title('Generador de archivos UAFE')
st.markdown('Completa los datos en cada sección y luego haz clic en _Guardar_ para registrar y subir archivos a Dropbox')

# 1. SECCIÓN: CABECERA
with st.expander('1. Cabecera', expanded=True):
    cdr = st.text_input('Código de Registro (CDR)', max_chars=5, key='cdr')
    pdr_date = st.date_input('Periodo de Reporte (PDR)', key='pdr_date')
    fre_date = st.date_input('Fecha de Corte (FRE)', key='fre_date')
    pdr = pdr_date.strftime("%Y%m%d")
    fre = fre_date.strftime("%Y%m%d")
    usr = st.text_input('Usuario (USR)', max_chars=20, key='usr')
    cli = st.number_input('Total Clientes (CLI)', min_value=0, step=1, key='cli')
    tro = st.number_input('Total Operaciones (TRO)', min_value=0, step=1, key='tro')
    tra = st.number_input('Total Transacciones (TRA)', min_value=0, step=1, key='tra')

    if st.button('Guardar Cabecera', key='save_cab'):
        registro = {'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
                    'CLI': cli, 'TRO': tro, 'TRA': tra}
        st.session_state.cabeceras.append(registro)
        st.success(f"✅ Cabecera guardada. Total en memoria: {len(st.session_state.cabeceras)}")

    if st.button('Exportar y Subir Cabeceras', key='exp_cab'):
        if not st.session_state.cabeceras:
            st.warning("No hay datos de Cabecera para exportar.")
        else:
            df = pd.DataFrame(st.session_state.cabeceras)
            df = df[df['PDR'].str[:6] == pdr[:6]]
            filename = f'CABECERA_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df.to_excel(buf, index=False)
            data = buf.getvalue()
            st.download_button("Descargar Cabeceras", data, filename,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key='dl_cab')
            url = upload_to_dropbox(data, filename)
            if url:
                st.success(f"Subido a Dropbox: {url}")

# 2. SECCIÓN: DETALLE CLIENTE
with st.expander('2. Detalle Cliente', expanded=False):
    tid = st.selectbox('Tipo Identificación (TID)', ['Cédula', 'RUC', 'Pasaporte'], key='tid_cli')
    ide = st.text_input('Identificación (IDE)', key='ide_cli')
    nrs = st.text_input('Nombres / Razón Social (NRS)', key='nrs_cli')
    nac = st.text_input('Nacionalidad (NAC)', key='nac_cli')
    dir_ = st.text_input('Dirección (DIR)', key='dir_cli')
    ccc = st.text_input('Cantón (CCC)', key='ccc_cli')
    aec = st.text_input('Actividad Económica (AEC)', key='aec_cli')
    imt = st.number_input('Ingreso Mensual (IMT)', min_value=0.0, key='imt_cli')

    if st.button('Guardar Cliente', key='save_cli'):
        registro = {'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
                    'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.clientes.append(registro)
        st.success(f"✅ Cliente guardado. Total en memoria: {len(st.session_state.clientes)}")

    if st.button('Exportar y Subir Clientes', key='exp_cli'):
        if not st.session_state.clientes:
            st.warning("No hay datos de Clientes para exportar.")
        else:
            df_cli = pd.DataFrame(st.session_state.clientes)
            df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_cli.to_excel(buf, index=False)
            data = buf.getvalue()
            st.download_button("Descargar Clientes", data, filename,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key='dl_cli')
            url = upload_to_dropbox(data, filename)
            if url:
                st.success(f"Subido a Dropbox: {url}")

# 3. SECCIÓN: DETALLE OPERACIÓN
with st.expander('3. Detalle Operación', expanded=False):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    nct = st.text_input('Número Operación/Contrato (NCT)', key='nct_op')
    vto = st.number_input('Valor Total Operación (VTO)', min_value=0.0, format='%.2f', key='vto_op')
    fdo_date = st.date_input('Fecha de Operación (FDO)', key='fdo_op')
    fdo = fdo_date.strftime('%Y%m%d')

    if st.button('Guardar Operación', key='save_op'):
        registro = {'TID': tid_op, 'IDE': ide_op, 'NCT': nct,
                    'VTO': vto, 'FDO': fdo,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.operaciones.append(registro)
        st.success(f"✅ Operación guardada. Total en memoria: {len(st.session_state.operaciones)}")

    if st.button('Exportar y Subir Operaciones', key='exp_op'):
        if not st.session_state.operaciones:
            st.warning("No hay datos de Operaciones para exportar.")
        else:
            df_op = pd.DataFrame(st.session_state.operaciones)
            df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_op.to_excel(buf, index=False)
            data = buf.getvalue()
            st.download_button("Descargar Operaciones", data, filename,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key='dl_op')
            url = upload_to_dropbox(data, filename)
            if url:
                st.success(f"Subido a Dropbox: {url}")

# 4. SECCIÓN: DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción', expanded=False):
    tid_tr = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación (IDE)', key='ide_tr')
    ctr = st.text_input('Código Transacción (CTR)', key='ctr_tr')
    ftr_date = st.date_input('Fecha Transacción (FTR)', key='ftr_tr')
    ftr = ftr_date.strftime('%Y%m%d')

    if st.button('Guardar Transacción', key='save_tr'):
        registro = {'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
                    'FTR': ftr,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.transacciones.append(registro)
        st.success(f"✅ Transacción guardada. Total en memoria: {len(st.session_state.transacciones)}")

    if st.button('Exportar y Subir Transacciones', key='exp_tr'):
        if not st.session_state.transacciones:
            st.warning("No hay datos de Transacciones para exportar.")
        else:
            df_tr = pd.DataFrame(st.session_state.transacciones)
            df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_tr.to_excel(buf, index=False)
            data = buf.getvalue()
            st.download_button("Descargar Transacciones", data, filename,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key='dl_tr')
            url = upload_to_dropbox(data, filename)
            if url:
                st.success(f"Subido a Dropbox: {url}")

# 5. CIERRE MENSUAL y REPORTERÍA GENERAL
st.markdown("---")
st.header('🔒 Cierre Mensual')
if st.button('Cerrar Mes', key='cierre_mes'):
    month = pdr[:6]
    sections = {
        'CABECERA': st.session_state.cabeceras,
        'DETALLECLIENTE': st.session_state.clientes,
        'DETALLEOPERACION': st.session_state.operaciones,
        'DETALLETRANSACCION': st.session_state.transacciones
    }
    for name, records in sections.items():
        if records:
            df = pd.DataFrame(records)
            df = df[df['PDR'].str[:6] == month]
            filename = f'{name}_{cdr}_{month}.xlsx'
            buf = BytesIO()
            df.to_excel(buf, index=False)
            data = buf.getvalue()
            st.download_button(f"Descargar {name}", data,
                               filename,
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key=f'dl_{name}')
            url = upload_to_dropbox(data, filename)
            if url:
                st.success(f"Subido a Dropbox: {url}")
    # Consolidado general
    all_buf = BytesIO()
    with pd.ExcelWriter(all_buf, engine='openpyxl') as writer:
        for name, records in sections.items():
            if records:
                pd.DataFrame(records).to_excel(writer, sheet_name=name, index=False)
    all_data = all_buf.getvalue()
    st.download_button('Descargar reportería general', all_data,
                       'reporteria_general.xlsx',
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key='dl_general')
    url_all = upload_to_dropbox(all_data, 'reporteria_general.xlsx')
    if url_all:
        st.success(f"Subido a Dropbox: {url_all}")
    # Limpieza de memoria
    for state_key in sections.keys():
        st.session_state[state_key.lower()].clear()
    st.success('✅ Cierre mensual completado.')
