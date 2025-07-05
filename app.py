import streamlit as st
import pandas as pd
from datetime import date
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

# Asegurar carpeta de salida
os.makedirs("documentos", exist_ok=True)

# Sección: Cabecera
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

    def guardar_cabecera():
        registro = {
            'CDR': cdr, 'PDR': pdr, 'FRE': fre, 'USR': usr,
            'CLI': cli, 'TRO': tro, 'TRA': tra,
            'TVO': tvo, 'TDE': tde, 'TCR': tcr,
            'TEF': tef, 'TCH': tch, 'TTC': ttc,
            'TVF': tvf, 'TCD': tcd, 'TCV': tcv, 'TVT': tvt
        }
        st.session_state.cabeceras.append(registro)
        st.success(f"✅ Cabecera guardada. En memoria: {len(st.session_state.cabeceras)}")
    st.button('Guardar Cabecera', on_click=guardar_cabecera, key='save_cab')

    def exportar_cabecera():
        df = pd.DataFrame(st.session_state.cabeceras)
        df = df[df['PDR'].str[:6] == pdr[:6]]
        out = os.path.join('documentos', f'CABECERA_{cdr}_{pdr[:6]}.xlsx')
        df.to_excel(out, index=False)
        st.success(f"✅ Exportados {len(df)} registros de Cabecera a: {out}")
    st.button('Exportar Cabeceras del Mes', on_click=exportar_cabecera, key='exp_cab')

# Sección: Detalle Cliente
with st.expander('2. Detalle Cliente'):
    tid = st.selectbox('Tipo Identificación (TID)', ['Cédula', 'RUC', 'Pasaporte'])
    ide = st.text_input('Identificación (IDE)')
    nrs = st.text_input('Nombres / Razón Social (NRS)')
    nac = st.text_input('Nacionalidad (NAC)')
    dir_ = st.text_input('Dirección (DIR)')
    ccc = st.text_input('Cantón (CCC)')
    aec = st.text_input('Actividad Económica (AEC)')
    imt = st.number_input('Ingreso Mensual (IMT)', min_value=0.0)
    st.write(f"Registro para CDR: **{cdr}** / Periodo: **{pdr[:6]}**")

    def guardar_cliente():
        registro = {
            'TID': tid, 'IDE': ide, 'NRS': nrs, 'NAC': nac,
            'DIR': dir_, 'CCC': ccc, 'AEC': aec, 'IMT': imt,
            'CDR': cdr, 'PDR': pdr
        }
        st.session_state.clientes.append(registro)
        st.success(f"✅ Cliente guardado. En memoria: {len(st.session_state.clientes)}")
    st.button('Guardar Cliente', on_click=guardar_cliente, key='save_cli')

    def exportar_clientes():
        df_cli = pd.DataFrame(st.session_state.clientes)
        df_cli = df_cli[df_cli['PDR'].str[:6] == pdr[:6]]
        out = os.path.join('documentos', f'DETALLECLIENTE_{cdr}_{pdr[:6]}.xlsx')
        df_cli.to_excel(out, index=False)
        st.success(f"✅ Exportados {len(df_cli)} clientes a: {out}")
    st.button('Exportar Clientes del Mes', on_click=exportar_clientes, key='exp_cli')

# Sección: Detalle Operación
with st.expander('3. Detalle Operación'):
    tid_op = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_op')
    ide_op = st.text_input('Identificación (IDE)', key='ide_op')
    nct = st.text_input('Número de Operación/Contrato (NCT)')
    vto = st.number_input('Valor Total Operación (VTO)', min_value=0.0, format='%.2f')
    fdo = st.date_input('Fecha de Operación (FDO)', key='fdo_op').strftime('%Y%m%d')
    vch = st.number_input('Valor Cheque (VCH)', min_value=0.0, format='%.2f')
    vtc = st.number_input('Valor Tarjeta Crédito (VTC)', min_value=0.0, format='%.2f')
    vfc = st.number_input('Valor Financiamiento (VFC)', min_value=0.0, format='%.2f')
    vcd = st.number_input('Valor Crédito Directo (VCD)', min_value=0.0, format='%.2f')
    vcv = st.number_input('Valor Contrato / Bien (VCV)', min_value=0.0, format='%.2f')
    vvt = st.number_input('Valor Total (VVT)', min_value=0.0, format='%.2f')
    mnd = st.selectbox('Moneda (MND)', ['USD','EUR','Otro'])
    ttr = st.selectbox('Tipo Transacción (TTR)', ['Venta','Crédito','Otro'])
    cat = st.text_input('Código Agencia (CAT)')
    rpt = st.selectbox('Pago con Recursos Propios/Terceros (RPT)', ['Propios','Terceros'])
    tit = st.selectbox('Tipo Identificación Tercero (TIT)', ['Cédula','RUC','Pasaporte','N/A'])
    idt = st.text_input('Identificación Tercero (IDT)')
    nrt = st.text_input('Nombre/Razón Social Tercero (NRT)')

    def guardar_operacion():
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
        st.success(f"✅ Operación guardada. En memoria: {len(st.session_state.operaciones)}")
    st.button('Guardar Operación', on_click=guardar_operacion, key='save_op')

    def exportar_operaciones():
        df_op = pd.DataFrame(st.session_state.operaciones)
        df_op = df_op[df_op['PDR'].str[:6] == pdr[:6]]
        out = os.path.join('documentos', f'DETALLEOPERACION_{cdr}_{pdr[:6]}.xlsx')
        df_op.to_excel(out, index=False)
        st.success(f"✅ Exportadas {len(df_op)} operaciones a: {out}")
    st.button('Exportar Operaciones del Mes', on_click=exportar_operaciones, key='exp_op')

# Sección: Detalle Transacción
with st.expander('4. Detalle Transacción'):
    tid_tr = st.selectbox('Tipo Identificación (TID)', ['Cédula','RUC','Pasaporte'], key='tid_tr')
    ide_tr = st.text_input('Identificación (IDE)', key='ide_tr')
    ctr = st.text_input('Código Transacción (CTR)')
    ftr = st.date_input('Fecha Transacción (FTR)', key='ftr_tr').strftime('%Y%m%d')
    vtr = st.number_input('Valor (VTR)', min_value=0.0, format='%.2f')
    mpg = st.selectbox('Medio de Pago (MPG)', ['Efectivo','Cheque','Tarjeta','Transferencia','Otro'])
    cat_tr = st.text_input('Código Agencia (CAT)', key='cat_tr')

    def guardar_transaccion():
        registro = {
            'TID': tid_tr, 'IDE': ide_tr, 'CTR': ctr,
            'FTR': ftr, 'VTR': vtr, 'MPG': mpg,
            'CAT': cat_tr, 'CDR': cdr, 'PDR': pdr
        }
        st.session_state.transacciones.append(registro)
        st.success(f"✅ Transacción guardada. En memoria: {len(st.session_state.transacciones)}")
    st.button('Guardar Transacción', on_click=guardar_transaccion, key='save_tr')

    def exportar_transacciones():
        df_tr = pd.DataFrame(st.session_state.transacciones)
        df_tr = df_tr[df_tr['PDR'].str[:6] == pdr[:6]]
        out = os.path.join('documentos', f'DETALLETRANSACCION_{cdr}_{pdr[:6]}.xlsx')
        df_tr.to_excel(out, index=False)
        st.success(f"✅ Exportadas {len(df_tr)} transacciones a: {out}")
    st.button('Exportar Transacciones del Mes', on_click=exportar_transacciones, key='exp_tr')

# 5. CIERRE MENSUAL y REPORTERÍA GENERAL
st.markdown("---")
st.header('🔒 Cierre Mensual')

def cierre_mensual():
    month = pdr[:6]
    sections = {
        'CABECERA': st.session_state.cabeceras,
        'DETALLECLIENTE': st.session_state.clientes,
        'DETALLEOPERACION': st.session_state.operaciones,
        'DETALLETRANSACCION': st.session_state.transacciones
    }
    # Generar Excel mensuales
    for prefix, records in sections.items():
        df = pd.DataFrame(records)
        if 'PDR' in df.columns:
            df = df[df['PDR'].str[:6] == month]
        path = os.path.join('documentos', f'{prefix}_{cdr}_{month}.xlsx')
        df.to_excel(path, index=False)
    # Generar reportería general
    rep_path = os.path.join('documentos', 'reporteria_general.xlsx')
    with pd.ExcelWriter(rep_path, engine='openpyxl', mode='w') as writer:
        for prefix, records in sections.items():
            df_all = pd.DataFrame(records)
            df_all.to_excel(writer, sheet_name=prefix, index=False)
    # Limpiar memoria para próximo mes
    for key in sections.keys():
        st.session_state[key].clear()
    st.success('✅ Cierre mensual completado. Archivos mensuales y general creados en documentos/')

st.button('Cerrar Mes', on_click=cierre_mensual, key='cierre_mes')
