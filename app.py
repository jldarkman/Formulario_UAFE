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
        registro = {
            'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
            'CLI': cli, 'TRO': tro, 'TRA': tra,
            'TVO': tvo, 'TDE': tde, 'TCR': tcr,
            'TEF': tef, 'TCH': tch, 'TTC': ttc,
            'TVF': tvf, 'TCD': tcd, 'TCV': tcv, 'TVT': tvt
        }
        st.session_state.cabeceras.append(registro)
        st.success(f"✅ Cabecera guardada. Total: {len(st.session_state.cabeceras)}")

    if st.button('Exportar Cabeceras del Mes', key='exp_cab'):
        if not st.session_state.cabeceras:
            st.warning("No hay datos de Cabecera para exportar.")
        else:
            df = pd.DataFrame(st.session_state.cabeceras)
            df = df[df['PDR'].str[:6] == pdr[:6]]
            download_excel(df, f'CABECERA_{cdr}_{pdr[:6]}.xlsx')

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
        registro = {
            'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
            'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
            'CDR': cdr, 'PDR': pdr
        }
        st.session_state.clientes.append(registro)
        st.success(f"✅ Cliente guardado. Total: {len(st.session_state.clientes)}")

    if st.button('Exportar Clientes del Mes', key='exp_cli'):
        if not st.session_state.clientes:
            st.warning("No hay datos de Clientes para exportar.")
        else:
            df_cli = pd.DataFrame(st.session_state.clientes)
            df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
            download_excel(df_cli, f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx')

# 3. SECCIÓN DETALLE OPERACIÓN
with st.expander('3. Detalle Operación', expanded=False):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    nct = st.text_input('Número de Operación/Contrato (NCT)', key='nct_op')
    vto = st.number_input('Valor Total Operación (VTO)', min_value=0.0, format='%.2f', key='vto_op')
    fdo_date = st.date_input('Fecha de Operación (FDO)', key='fdo_op')
    fdo = fdo_date.strftime('%Y%m%d')
    vch = st.number_input('Valor Cheque (VCH)', min_value=0.0, format='%.2f', key='vch_op')
    vtc = st.number_input('Valor Tarjeta Crédito (VTC)', min_value=0.0, format='%.2f', key='vtc_op')
    vfc = st.number_input('Valor Financiamiento (VFC)', min_value=0.0, format='%.2f', key='vfc_op')
    vcd = st.number_input('Valor Crédito Directo (VCD)', min_value=0.0, format='%.2f', key='vcd_op')
    vcv = st.number_input('Valor Contrato / Bien (VCV)', min_value=0.0, format='%.2f', key='vcv_op')
    vvt = st.number_input('Valor Total (VVT)', min_value=0.0, format='%.2f', key='vvt_op')
    mnd = st.selectbox('Moneda (MND)', ['USD','EUR','Otro'], key='mnd_op')
    ttr = st.selectbox('Tipo Transacción (TTR)', ['Venta','Crédito','Otro'], key='ttr_op')
    cat = st.text_input('Código Agencia (CAT)', key='cat_op')
    rpt = st.selectbox('Pago con Recursos Propios/Terceros (RPT)', ['Propios','Terceros'], key='rpt_op')
    tit = st.selectbox('Tipo Identificación Tercero (TIT)', ['Cédula','RUC','Pasaporte','N/A'], key='tit_op')
    idt = st.text_input('Identificación Tercero (IDT)', key='idt_op')
    nrt = st.text_input('Nombre/Razón Social Tercero (NRT)', key='nrt_op')

    if st.button('Guardar Operación', key='save_op'):
        registro = {
            'TID': tid_op, 'IDE': ide_op, 'NCT': nct,
            'VTO': vto, 'FDO': fdo,
            'VCH': vch, 'VTC': vtc, 'VFC': vfc,
            'VCD': vcd, 'VCV': vcv, 'VVT': vvt,
            'MND': mnd, 'TTR': ttr, 'CAT': cat,
            'RPT': rpt, 'TIT': tit, 'IDT': idt,
            'NRT': nrt, 'CDR': cdr, 'PDR': pdr
        }
        st.session_state.operaciones.append(registro)
        st.success(f"✅ Operación guardada. Total: {len(st.session_state.operaciones)}")

    if st.button('Exportar Operaciones del Mes', key='exp_op'):
        if not st.session_state.operaciones:
            st.warning("No hay datos de Operaciones para exportar.")
        else:
            df_op = pd.DataFrame(st.session_state.operaciones)
            df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
            download_excel(df_op, f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx')

# 4. SECCIÓN DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción', expanded=False):
    tid_tr = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación (IDE)', key='ide_tr')
    ctr = st.text_input('Código Transacción (CTR)', key='ctr_tr')
    ftr_date = st.date_input('Fecha Transacción (FTR)', key='ftr_tr')
    ftr = ftr_date.strftime('%Y%m%d')
    vtr = st.number_input('Valor (VTR)', min_value=0.0, format='%.2f', key='vtr_tr')
    mpg = st.selectbox('Medio de Pago (MPG)', ['Efectivo','Cheque','Tarjeta','Transferencia','Otro'], key='mpg_tr')
    cat_tr = st.text_input('Código Agencia (CAT)', key='cat_tr')

    if st.button('Guardar Transacción', key='save_tr'):
        registro = {
            'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
            'FTR': ftr, 'VTR': vtr, 'MPG': mpg,
            'CAT': cat_tr, 'CDR': cdr, 'PDR': pdr
        }
        st.session_state.transacciones.append(registro)
        st.success(f"✅ Transacción guardada. Total: {len(st.session_state.transacciones)}")

    if st.button('Exportar Transacciones del Mes', key='exp_tr'):
        if not st.session_state.transacciones:
            st.warning("No hay datos de Transacciones para exportar.")
        else:
            df_tr = pd.DataFrame(st.session_state.transacciones)
            df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
            download_excel(df_tr, f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx')

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
            download_excel(df, f'{name}_{cdr}_{month}.xlsx')
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
