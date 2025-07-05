import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import os

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
st.markdown('Completa los datos en cada sección y luego haz clic en _Guardar_ para registrar la información')

# Función para descarga de Excel
os.makedirs("documentos", exist_ok=True)
def download_excel(df: pd.DataFrame, filename: str):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label=f"Descargar {filename}",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# 1. CABECERA
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
        registro = {'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
                    'CLI': cli, 'TRO': tro, 'TRA': tra,
                    'TVO': tvo, 'TDE': tde, 'TCR': tcr,
                    'TEF': tef, 'TCH': tch, 'TTC': ttc,
                    'TVF': tvf, 'TCD': tcd, 'TCV': tcv, 'TVT': tvt}
        st.session_state.cabeceras.append(registro)
        st.info(f"Cabecera guardada. Registros en memoria: {len(st.session_state.cabeceras)}")

    if st.button('Exportar Cabeceras del Mes', key='exp_cab'):
        df = pd.DataFrame(st.session_state.cabeceras)
        df = df[df['PDR'].str[:6] == pdr[:6]]
        filename = f'CABECERA_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df, filename)

# 2. DETALLE CLIENTE
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
        registro = {'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
                    'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.clientes.append(registro)
        st.info(f"Cliente guardado. Registros en memoria: {len(st.session_state.clientes)}")

    if st.button('Exportar Clientes del Mes', key='exp_cli'):
        df_cli = pd.DataFrame(st.session_state.clientes)
        df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_cli, filename)

# 3. DETALLE OPERACIÓN
with st.expander('3. Detalle Operación', expanded=False):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    nct = st.text_input('Número de Operación/Contrato (NCT)', key='nct_op')
    vto = st.number_input('Valor Operación', min_value=0.0, format='%.2f', key='vto_op')
    fdo = st.date_input('Fecha Operación', key='fdo_op').strftime('%Y%m%d')
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
    idt = st.text_input('ID Tercero', key='idt_op')
    nrt = st.text_input('Nombre Tercero', key='nrt_op')

    if st.button('Guardar Operación', key='save_op'):
        registro = {'TID': tid_op, 'IDE': ide_op, 'NCT': nct,
                    'VTO': vto, 'FDO': fdo, 'VCH': vch, 'VTC': vtc,
                    'VFC': vfc, 'VCD': vcd, 'VCV': vcv, 'VVT': vvt,
                    'MND': mnd, 'TTR': ttr, 'CAT': cat, 'RPT': rpt,
                    'TIT': tit, 'IDT': idt, 'NRT': nrt,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.operaciones.append(registro)
        st.info(f"Operación guardada. Registros en memoria: {len(st.session_state.operaciones)}")

    if st.button('Exportar Operaciones del Mes', key='exp_op'):
        df_op = pd.DataFrame(st.session_state.operaciones)
        df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_op, filename)

# 4. DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción', expanded=False):
    tid_tr = st.selectbox('Tipo ID', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación', key='ide_tr')
    ctr = st.text_input('Código Transacción', key='ctr_tr')
    ftr = st.date_input('Fecha Transacción', key='ftr_tr').strftime('%Y%m%d')
    vtr = st.number_input('Valor', min_value=0.0, format='%.2f', key='vtr_tr')
    mpg = st.selectbox('Medio de Pago', ['Efectivo','Cheque','Tarjeta','Transferencia','Otro'], key='mpg_tr')
    cat_tr = st.text_input('Código Agencia', key='cat_tr')

    if st.button('Guardar Transacción', key='save_tr'):
        registro = {'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
                    'FTR': ftr, 'VTR': vtr, 'MPG': mpg,
                    'CAT': cat_tr, 'CDR': cdr, 'PDR': pdr}
        st.session_state.transacciones.append(registro)
        st.info(f"Transacción guardada. Registros en memoria: {len(st.session_state.transacciones)}")

    if st.button('Exportar Transacciones del Mes', key='exp_tr'):
        df_tr = pd.DataFrame(st.session_state.transacciones)
        df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_tr, filename)

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
    # Generar y descargar mensuales
    for prefix, records in sections.items():
        df = pd.DataFrame(records)
        if 'PDR' in df.columns:
            df = df[df['PDR'].str[:6] == month]
        download_excel(df, f'{prefix}_{cdr}_{month}.xlsx')
    # Consolidado general
    all_buffer = BytesIO()
    with pd.ExcelWriter(all_buffer, engine='openpyxl') as writer:
        for prefix, records in sections.items():
            pd.DataFrame(records).to_excel(writer, sheet_name=prefix, index=False)
    all_buffer.seek(0)
    st.download_button(
        label='Descargar reportería general',
        data=all_buffer,
        file_name='reporteria_general.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # Limpiar memoria
    for key in sections.keys():
        st.session_state[key].clear()
    st.success('✅ Cierre mensual completado.')
