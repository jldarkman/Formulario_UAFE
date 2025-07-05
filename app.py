import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ---------- Configuración Google Drive ----------
# En tu archivo .streamlit/secrets.toml define:
# [gcp_service_account]
# type = "service_account"
# project_id = "..."
# private_key_id = "..."
# private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
# client_email = "..."
# client_id = "..."
# auth_uri = "https://accounts.google.com/o/oauth2/auth"
# token_uri = "https://oauth2.googleapis.com/token"
# auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
# client_x509_cert_url = "..."
# [gdrive]
# folder_id = "TU_FOLDER_ID"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=creds)
drive_folder_id = st.secrets["gdrive"]["folder_id"]

# ---------- Funciones auxiliares ----------

def upload_to_drive(buffer: BytesIO, filename: str) -> str:
    buffer.seek(0)
    media = MediaIoBaseUpload(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=True
    )
    metadata = {"name": filename, "parents": [drive_folder_id]}
    file = drive_service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()
    return file.get("id")

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
st.markdown('Completa los datos en cada sección y luego haz clic en _Guardar_ para registrar y subir a Google Drive')

# 1. SECCIÓN CABECERA
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
    tvo = st.number_input('Suma Valor Operaciones (TVO)', min_value=0, step=1, key='tvo')
    tde = st.number_input('Detalles de Operación (TDE)', min_value=0, step=1, key='tde')
    tcr = st.number_input('Total Crédito (TCR)', min_value=0, step=1, key='tcr')
    tef = st.number_input('Total Efectivo (TEF)', min_value=0, step=1, key='tef')
    tch = st.number_input('Total Cheque (TCH)', min_value=0, step=1, key='tch')
    ttc = st.number_input('Total Tarjeta Crédito (TTC)', min_value=0, step=1, key='ttc')
    tvf = st.number_input('Total Financiamiento (TVF)', min_value=0, step=1, key='tvf')
    tcd = st.number_input('Total Crédito Directo (TCD)', min_value=0, step=1, key='tcd')
    tcv = st.number_input('Total Contratos (TCV)', min_value=0, step=1, key='tcv')
    tvt = st.number_input('Valor Total (TVT)', min_value=0, step=1, key='tvt')

    if st.button('Guardar Cabecera', key='save_cab'):
        registro = { 'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
                     'CLI': cli, 'TRO': tro, 'TRA': tra,
                     'TVO': tvo, 'TDE': tde, 'TCR': tcr,
                     'TEF': tef, 'TCH': tch, 'TTC': ttc,
                     'TVF': tvf, 'TCD': tcd, 'TCV': tcv, 'TVT': tvt }
        st.session_state.cabeceras.append(registro)
        st.success(f"✅ Cabecera guardada. Total: {len(st.session_state.cabeceras)}")

    if st.button('Exportar y Subir Cabeceras', key='exp_cab'):
        if not st.session_state.cabeceras:
            st.warning("No hay datos de Cabecera para exportar.")
        else:
            df = pd.DataFrame(st.session_state.cabeceras)
            df = df[df['PDR'].str[:6] == pdr[:6]]
            filename = f'CABECERA_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df.to_excel(buf, index=False)
            buf.seek(0)
            st.download_button("Descargar Cabeceras", buf, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file_id = upload_to_drive(buf, filename)
            st.info(f"Subido a Google Drive: https://drive.google.com/file/d/{file_id}")

# 2. SECCIÓN DETALLE CLIENTE
with st.expander('2. Detalle Cliente', expanded=False):
    tid = st.selectbox('Tipo Identificación (TID)', ['Cédula', 'RUC', 'Pasaporte'], key='tid_cli')
    ide = st.text_input('Identificación (IDE)', key='ide_cli')
    nrs = st.text_input('Nombres / Razón Social (NRS)', key='nrs_cli')
    nac = st.text_input('Nacionalidad (NAC)', key='nac_cli')
    dir_ = st.text_input('Dirección (DIR)', key='dir_cli')
    ccc = st.text_input('Cantón (CCC)', key='ccc_cli')
    aec = st.text_input('Actividad Económica (AEC)', key='aec_cli')
    imt = st.number_input('Ingreso Mensual (IMT)', min_value=0.0, key='imt_cli')
    st.write(f"CDR: **{cdr}**, Periodo: **{pdr[:6]}**")

    if st.button('Guardar Cliente', key='save_cli'):
        registro = { 'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
                     'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
                     'CDR': cdr, 'PDR': pdr }
        st.session_state.clientes.append(registro)
        st.success(f"✅ Cliente guardado. Total: {len(st.session_state.clientes)}")

    if st.button('Exportar y Subir Clientes', key='exp_cli'):
        if not st.session_state.clientes:
            st.warning("No hay datos de Clientes para exportar.")
        else:
            df_cli = pd.DataFrame(st.session_state.clientes)
            df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_cli.to_excel(buf, index=False)
            buf.seek(0)
            st.download_button("Descargar Clientes", buf, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file_id = upload_to_drive(buf, filename)
            st.info(f"Subido a Google Drive: https://drive.google.com/file/d/{file_id}")

# 3. SECCIÓN DETALLE OPERACIÓN
with st.expander('3. Detalle Operación', expanded=False):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    nct = st.text_input('Número de Operación/Contrato (NCT)', key='nct_op')
    vto = st.number_input('Valor Total Operación', min_value=0.0, format='%.2f', key='vto_op')
    fdo_date = st.date_input('Fecha de Operación', key='fdo_op')
    fdo = fdo_date.strftime('%Y%m%d')
    vch = st.number_input('Valor Cheque', min_value=0.0, format='%.2f', key='vch_op')
    vtc = st.number_input('Valor Tarjeta', min_value=0.0, format='%.2f', key='vtc_op')
    vfc = st.number_input('Valor Financiamiento', min_value=0.0, format='%.2f', key='vfc_op')
    vcd = st.number_input('Valor Crédito Directo', min_value=0.0, format='%.2f', key='vcd_op')
    vcv = st.number_input('Valor Contrato/Bien', min_value=0.0, format='%.2f', key='vcv_op')
    vvt = st.number_input('Valor Total', min_value=0.0, format='%.2f', key='vvt_op')
    mnd = st.selectbox('Moneda', ['USD','EUR','Otro'], key='mnd_op')
    ttr = st.selectbox('Tipo Transacción', ['Venta','Crédito','Otro'], key='ttr_op')
    cat = st.text_input('Código Agencia', key='cat_op')
    rpt = st.selectbox('Recursos Propios/Terceros', ['Propios','Terceros'], key='rpt_op')
    tit = st.selectbox('Tipo ID Tercero', ['Cédula','RUC','Pasaporte','N/A'], key='tit_op')
    idt = st.text_input('Identificación Tercero', key='idt_op')
    nrt = st.text_input('Nombre Tercero', key='nrt_op')

    if st.button('Guardar Operación', key='save_op'):
        registro = { 'TID': tid_op, 'IDE': ide_op, 'NCT': nct,
                     'VTO': vto, 'FDO': fdo,
                     'VCH': vch, 'VTC': vtc, 'VFC': vfc,
                     'VCD': vcd, 'VCV': vcv, 'VVT': vvt,
                     'MND': mnd, 'TTR': ttr, 'CAT': cat,
                     'RPT': rpt, 'TIT': tit, 'IDT': idt,
                     'NRT': nrt, 'CDR': cdr, 'PDR': pdr }
        st.session_state.operaciones.append(registro)
        st.success(f"✅ Operación guardada. Total: {len(st.session_state.operaciones)}")

    if st.button('Exportar y Subir Operaciones', key='exp_op'):
        if not st.session_state.operaciones:
            st.warning("No hay datos de Operaciones para exportar.")
        else:
            df_op = pd.DataFrame(st.session_state.operaciones)
            df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_op.to_excel(buf, index=False)
            buf.seek(0)
            st.download_button("Descargar Operaciones", buf, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file_id = upload_to_drive(buf, filename)
            st.info(f"Subido a Google Drive: https://drive.google.com/file/d/{file_id}")

# 4. SECCIÓN DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción', expanded=False):
    tid_tr = st.selectbox('Tipo ID', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación', key='ide_tr')
    ctr = st.text_input('Código Transacción', key='ctr_tr')
    ftr_date = st.date_input('Fecha Transacción', key='ftr_tr')
    ftr = ftr_date.strftime('%Y%m%d')
    vtr = st.number_input('Valor', min_value=0.0, format='%.2f', key='vtr_tr')
    mpg = st.selectbox('Medio de Pago', ['Efectivo','Cheque','Tarjeta','Transferencia','Otro'], key='mpg_tr')
    cat_tr = st.text_input('Código Agencia', key='cat_tr')

    if st.button('Guardar Transacción', key='save_tr'):
        registro = { 'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
                     'FTR': ftr, 'VTR': vtr, 'MPG': mpg,
                     'CAT': cat_tr, 'CDR': cdr, 'PDR': pdr }
        st.session_state.transacciones.append(registro)
        st.success(f"✅ Transacción guardada. Total: {len(st.session_state.transacciones)}")

    if st.button('Exportar y Subir Transacciones', key='exp_tr'):
        if not st.session_state.transacciones:
            st.warning("No hay datos de Transacciones para exportar.")
        else:
            df_tr = pd.DataFrame(st.session_state.transacciones)
            df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
            filename = f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx'
            buf = BytesIO()
            df_tr.to_excel(buf, index=False)
            buf.seek(0)
            st.download_button("Descargar Transacciones", buf, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file_id = upload_to_drive(buf, filename)
            st.info(f"Subido a Google Drive: https://drive.google.com/file/d/{file_id}")

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
            buf.seek(0)
            st.download_button(f"Descargar {name}", buf, filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file_id = upload_to_drive(buf, filename)
            st.info(f"Subido a Google Drive: https://drive.google.com/file/d/{file_id}")
    # Consolidado general
    all_buffer = BytesIO()
    with pd.ExcelWriter(all_buffer, engine='openpyxl') as writer:
        for name, records in sections.items():
            if records:
                pd.DataFrame(records).to_excel(writer, sheet_name=name, index=False)
    all_buffer.seek(0)
    st.download_button(
        label='Descargar reportería general',
        data=all_buffer,
        file_name='reporteria_general.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='download_general'
    )
    # Limpieza
    for state_key in ['cabeceras', 'clientes', 'operaciones', 'transacciones']:
        st.session_state[state_key].clear()
    st.success('✅ Cierre mensual completado.')
