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

# Asegurar carpeta de salida local (opcional)
os.makedirs("documentos", exist_ok=True)

# Función común para descargar DataFrame como Excel
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
    cdr = st.text_input('Código de Registro (CDR)', max_chars=5)
    pdr_date = st.date_input('Periodo de Reporte (PDR)')
    fre_date = st.date_input('Fecha de Corte (FRE)')
    pdr = pdr_date.strftime("%Y%m%d")
    fre = fre_date.strftime("%Y%m%d")
    usr = st.text_input('Usuario (USR)', max_chars=20)
    cli = st.number_input('Total Clientes (CLI)', min_value=0, step=1)
    tro = st.number_input('Total Operaciones (TRO)', min_value=0, step=1)
    tra = st.number_input('Total Transacciones (TRA)', min_value=0, step=1)
    tvo = st.number_input('Suma Valor Operaciones (TVO)', min_value=0, step=1)
    tde = st.number_input('Detalles de Operación (TDE)', min_value=0, step=1)
    tcr = st.number_input('Total Crédito (TCR)', min_value=0, step=1)
    tef = st.number_input('Total Efectivo (TEF)', min_value=0, step=1)
    tch = st.number_input('Total Cheque (TCH)', min_value=0, step=1)
    ttc = st.number_input('Total Tarjeta Crédito (TTC)', min_value=0, step=1)
    tvf = st.number_input('Total Financiamiento (TVF)', min_value=0, step=1)
    tcd = st.number_input('Total Crédito Directo (TCD)', min_value=0, step=1)
    tcv = st.number_input('Total Contratos (TCV)', min_value=0, step=1)
    tvt = st.number_input('Valor Total (TVT)', min_value=0, step=1)

    if st.button('Guardar Cabecera'):
        registro = {'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
                    'CLI': cli, 'TRO': tro, 'TRA': tra,
                    'TVO': tvo, 'TDE': tde, 'TCR': tcr,
                    'TEF': tef, 'TCH': tch, 'TTC': ttc,
                    'TVF': tvf, 'TCD': tcd, 'TCV': tcv, 'TVT': tvt}
        st.session_state.cabeceras.append(registro)
        st.info(f"Cabecera guardada. Registros en memoria: {len(st.session_state.cabeceras)}")

    if st.button('Exportar Cabeceras del Mes'):
        df = pd.DataFrame(st.session_state.cabeceras)
        df = df[df['PDR'].str[:6] == pdr[:6]]
        filename = f'CABECERA_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df, filename)

# 2. DETALLE CLIENTE
with st.expander('2. Detalle Cliente'):
    tid = st.selectbox('Tipo Identificación (TID)', ['Cédula', 'RUC', 'Pasaporte'])
    ide = st.text_input('Identificación (IDE)')
    nrs = st.text_input('Nombres / Razón Social (NRS)')
    nac = st.text_input('Nacionalidad (NAC)')
    dir_ = st.text_input('Dirección (DIR)')
    ccc = st.text_input('Cantón (CCC)')
    aec = st.text_input('Actividad Económica (AEC)')
    imt = st.number_input('Ingreso Mensual (IMT)', min_value=0.0)
    st.write(f"CDR: **{cdr}**, Periodo: **{pdr[:6]}**")

    if st.button('Guardar Cliente'):
        registro = {'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
                    'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.clientes.append(registro)
        st.info(f"Cliente guardado. Registros en memoria: {len(st.session_state.clientes)}")

    if st.button('Exportar Clientes del Mes'):
        df_cli = pd.DataFrame(st.session_state.clientes)
        df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_cli, filename)

# 3. DETALLE OPERACIÓN
with st.expander('3. Detalle Operación'):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'])
    ide_op = st.text_input('Identificación (IDE)')
    nct = st.text_input('Número de Operación/Contrato (NCT)')
    vto = st.number_input('Valor Operación', min_value=0.0, format='%.2f')
    fdo = st.date_input('Fecha Operación').strftime('%Y%m%d')
    vch = st.number_input('Valor Cheque', min_value=0.0, format='%.2f')
    vtc = st.number_input('Valor Tarjeta', min_value=0.0, format='%.2f')
    vfc = st.number_input('Valor Financiamiento', min_value=0.0, format='%.2f')
    vcd = st.number_input('Valor Crédito Directo', min_value=0.0, format='%.2f')
    vcv = st.number_input('Valor Contrato/Bien', min_value=0.0, format='%.2f')
    vvt = st.number_input('Valor Total', min_value=0.0, format='%.2f')
    mnd = st.selectbox('Moneda', ['USD','EUR','Otro'])
    ttr = st.selectbox('Tipo Transacción', ['Venta','Crédito','Otro'])
    cat = st.text_input('Código Agencia')
    rpt = st.selectbox('Recursos Propios/Terceros', ['Propios','Terceros'])
    tit = st.selectbox('Tipo ID Tercero', ['Cédula','RUC','Pasaporte','N/A'])
    idt = st.text_input('ID Tercero')
    nrt = st.text_input('Nombre Tercero')

    if st.button('Guardar Operación'):
        registro = {'TID': tid_op, 'IDE': ide_op, 'NCT': nct,
                    'VTO': vto, 'FDO': fdo, 'VCH': vch, 'VTC': vtc,
                    'VFC': vfc, 'VCD': vcd, 'VCV': vcv, 'VVT': vvt,
                    'MND': mnd, 'TTR': ttr, 'CAT': cat, 'RPT': rpt,
                    'TIT': tit, 'IDT': idt, 'NRT': nrt,
                    'CDR': cdr, 'PDR': pdr}
        st.session_state.operaciones.append(registro)
        st.info(f"Operación guardada. Registros en memoria: {len(st.session_state.operaciones)}")

    if st.button('Exportar Operaciones del Mes'):
        df_op = pd.DataFrame(st.session_state.operaciones)
        df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_op, filename)

# 4. DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción'):
    tid_tr = st.selectbox('Tipo ID', ['Cédula','RUC','Pasaporte'])
    ide_tr = st.text_input('Identificación')
    ctr = st.text_input('Código Transacción')
    ftr = st.date_input('Fecha Transacción').strftime('%Y%m%d')
    vtr = st.number_input('Valor', min_value=0.0, format='%.2f')
    mpg = st.selectbox('Medio de Pago', ['Efectivo','Cheque','Tarjeta','Transferencia','Otro'])
    cat_tr = st.text_input('Código Agencia')

    if st.button('Guardar Transacción'):
        registro = {'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
                    'FTR': ftr, 'VTR': vtr, 'MPG': mpg,
                    'CAT': cat_tr, 'CDR': cdr, 'PDR': pdr}
        st.session_state.transacciones.append(registro)
        st.info(f"Transacción guardada. Registros en memoria: {len(st.session_state.transacciones)}")

    if st.button('Exportar Transacciones del Mes'):
        df_tr = pd.DataFrame(st.session_state.transacciones)
        df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
        filename = f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx'
        download_excel(df_tr, filename)

# 5. CIERRE MENSUAL y REPORTERÍA GENERAL
st.markdown("---")
st.header('🔒 Cierre Mensual')

if st.button('Cerrar Mes'):
    month = pdr[:6]
    sections = {
        'CABECERA': st.session_state.cabeceras,
        'DETALLECLIENTE': st.session_state.clientes,
        'DETALLEOPERACION': st.session_state.operaciones,
        'DETALLETRANSACCION': st.session_state.transacciones
    }
    # Generar Excel mensuales y descarga
    for prefix, records in sections.items():
        df = pd.DataFrame(records)
        if 'PDR' in df.columns:
            df = df[df['PDR'].str[:6] == month]
        filename = f'{prefix}_{cdr}_{month}.xlsx'
        download_excel(df, filename)
    # Generar reportería general
    all_writer = BytesIO()
    with pd.ExcelWriter(all_writer, engine='openpyxl') as writer:
        for prefix, records in sections.items():
            pd.DataFrame(records).to_excel(writer, sheet_name=prefix, index=False)
    all_writer.seek(0)
    st.download_button(
        label='Descargar reportería general',
        data=all_writer,
        file_name='reporteria_general.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # Limpiar memoria
    for key in sections.keys():
        st.session_state[key].clear()
    st.success('✅ Cierre mensual completado.')
