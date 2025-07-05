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
    # ... otros inputs con key ...

    if st.button('Guardar Cabecera', key='save_cab'):
        registro = {'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
                    'CLI': cli, 'TRO': tro, 'TRA': tra}
        st.session_state.cabeceras.append(registro)
        st.info(f"Cabecera guardada. Registros en memoria: {len(st.session_state.cabeceras)}")

    if st.button('Exportar Cabeceras del Mes', key='exp_cab'):
        if not st.session_state.cabeceras:
            st.warning("No hay registros de Cabecera para exportar.")
        else:
            df = pd.DataFrame(st.session_state.cabeceras)
            if 'PDR' in df.columns:
                df = df[df['PDR'].str[:6] == pdr[:6]]
            download_excel(df, f'CABECERA_{cdr}_{pdr[:6]}.xlsx')

# 2. DETALLE CLIENTE
with st.expander('2. Detalle Cliente', expanded=False):
    tid = st.selectbox('Tipo Identificación (TID)', ['Cédula', 'RUC', 'Pasaporte'], key='tid_cli')
    ide = st.text_input('Identificación (IDE)', key='ide_cli')
    # ... otros inputs con key ...

    if st.button('Guardar Cliente', key='save_cli'):
        registro = {'TID': tid, 'IDE': ide, 'CDR': cdr, 'PDR': pdr}
        st.session_state.clientes.append(registro)
        st.info(f"Cliente guardado. Registros en memoria: {len(st.session_state.clientes)}")

    if st.button('Exportar Clientes del Mes', key='exp_cli'):
        if not st.session_state.clientes:
            st.warning("No hay clientes para exportar.")
        else:
            df_cli = pd.DataFrame(st.session_state.clientes)
            if 'PDR' in df_cli.columns:
                df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
            download_excel(df_cli, f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx')

# 3. DETALLE OPERACIÓN
with st.expander('3. Detalle Operación', expanded=False):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    # ... otros inputs con key ...

    if st.button('Guardar Operación', key='save_op'):
        registro = {'TID': tid_op, 'IDE': ide_op, 'CDR': cdr, 'PDR': pdr}
        st.session_state.operaciones.append(registro)
        st.info(f"Operación guardada. Registros en memoria: {len(st.session_state.operaciones)}")

    if st.button('Exportar Operaciones del Mes', key='exp_op'):
        if not st.session_state.operaciones:
            st.warning("No hay operaciones para exportar.")
        else:
            df_op = pd.DataFrame(st.session_state.operaciones)
            if 'PDR' in df_op.columns:
                df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
            download_excel(df_op, f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx')

# 4. DETALLE TRANSACCIÓN
with st.expander('4. Detalle Transacción', expanded=False):
    tid_tr = st.selectbox('Tipo ID', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación', key='ide_tr')
    # ... otros inputs con key ...

    if st.button('Guardar Transacción', key='save_tr'):
        registro = {'TID': tid_tr, 'IDE': ide_tr, 'CDR': cdr, 'PDR': pdr}
        st.session_state.transacciones.append(registro)
        st.info(f"Transacción guardada. Registros en memoria: {len(st.session_state.transacciones)}")

    if st.button('Exportar Transacciones del Mes', key='exp_tr'):
        if not st.session_state.transacciones:
            st.warning("No hay transacciones para exportar.")
        else:
            df_tr = pd.DataFrame(st.session_state.transacciones)
            if 'PDR' in df_tr.columns:
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
            if 'PDR' in df.columns:
                df = df[df['PDR'].str[:6] == month]
            download_excel(df, f'{name}_{cdr}_{month}.xlsx')
    # Consolidado general en memoria
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
