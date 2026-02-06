import streamlit as st
from streamlit_autorefresh import st_autorefresh
from db import load_data
import pandas as pd

# --- Automatický refresh ---
st_autorefresh(interval=5*60*1000, key="dashboard_refresh")
st.set_page_config(page_title="Skladový Dashboard", layout="wide")

# --- CSS štýly ---
st.markdown(
    """
    <style>
    div[data-testid="stApp"] { background-color: #191919 !important; }

    /* Odstránenie medzier Streamlit okolo hlavného kontajnera */
    div[data-testid="stApp"] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    /* Nadpis dashboardu úplne hore */
    .dashboard-title {
        position: fixed;      /* fixed, aby ostal pri scrollovaní */
        top: 50px;
        left: 0px;
        width: 100%;
        text-align: center;
        color: white;
        background-color: #102B5D;
        font-size: 50px;
        font-weight: bold;
        padding: 10px 0;
        margin: 0;
        z-index: 1000;
    }

    /* Tabuľky s absolútnou pozíciou */
    .table-container {
        position: absolute;
        width: 275px;       /* šírka tabuľky */
    }

    .table-title {
        color: white;
        background-color: #102B5D;
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        width: 100%;
        margin: 0;
        padding: 0;
    }

    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0;
    }

    .custom-table th {
        background-color: #102B5D;
        color: white;
        font-weight: bold;
        font-size: 40px;
        text-align: center;
        padding: 0;
    }

    .custom-table td {
        background-color: #00aeef;
        color: white;
        font-weight: bold;
        font-size: 40px;
        text-align: center;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Logo úplne dole vpravo ---
st.markdown(
    """
    <img id="fixed-logo" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQAAABZCAMAAACXK/MtAAAAn1BMVEUAAAAQK10QK10QK10QK10Aru8Aru8QK10GebIAru8QK10Aru8QK10Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8Aru8QK10Aru8QK10Aru8Aru8Aru8QK10Aru8Aru8QK10Aru8QK10QK10Aru8Aru8QK10Aru8QK10QK10QK10QK10QK10QK10Aru93p3r+AAAAM3RSTlMAIK3QoPoR7ATyLSGIwOmojl8bMAriPyquntJ/cAvZ1pV5TOTMRvbFvJiJbF9VF2lFfE+bUO++AAACXElEQVRYw+3Yy3LaQBCF4VYM4iKEkGQJC1lcTEJih2Anmvd/tlScwV2oJ4zVp7JIVc7Os/g2/puF6N/ZyrxuQXbNvlVsP71A5+b3dvbv8abVbHShPhm71D4EI1xdntHhJ/syPeDqx7M6ye3LjxZWv5rz5pF9eobVcPimrkP7NoPVxLzt8619G6Dqg+HdjW1YX0B1PDe87fkGNoDKqXaOINgDKqfaOYLpSK1yquIIXg5KNSBOVRzBsdVtQJyqPILj4J0bXaAf6HV3LPIR9NiNRDlVPgIc5VT5CHCUFqazLYxyqrwdjHKqvBRHOVU+AgQVqfIRAKhIlY8AQDlVcQQAyqmKIwBQTlUcAYTmxrUtgHKq4ggw9N44lwIopyqOAEA5VXEEAMqpiiPQopyq3DrXo5yq7DVXo5yqXLJUorQyV1ZFClSkKuKqMg0axuY6u836ozTeDT3sIuyD2uVrc32TtD9KtfEs6Y1msYec1GFf9GHuIZ8E6UVLxX/JiyaKnnzo7cRTvgZNPTeqQmPPr4kGjf5k3hP1RP3ZLwhAC88F9UB9kcZjBHVHugoJQN2RFhkBqDvSyZIA1B3psCQEdUf6jTC0dkYPooUrehAtXdGjaOWIHkA5UhE9iKaO6GE0ltHDaCSjx9FaRo+jhTv6JnjnNg60dEd/UnyaY7RyRt/ctLo9y0hj8MNk+8iRiugfIZNiV/TfleaMIxXRHzGTakf0LwfMpEJGPx2BZimjD/agSZWIvtmgJkeaEAeKmZSKX/oBbFLcjX6GmzTsRN/oTV4Y/VrGX7VOgWIn+r+/u5/Kg/cwH09yBQAAAABJRU5ErkJggg==" 
         style="
            position: fixed;
            bottom: 40px;       /* 40px od spodku */
            right: 40px;        /* 40px od pravého okraja */
            height: 100px;       /* výška loga 200px */
            width: auto;        /* zachovať proporcie */
            z-index: 9999;
         ">
    """,
    unsafe_allow_html=True
)

# --- Nadpis dashboardu ---
st.markdown('<div class="dashboard-title">SKLADOVÝ DASHBOARD 🛒📦</div>', unsafe_allow_html=True)

# --- SQL dotazy ---
sql1 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and  NOT B.DOK like 'SO%' and  NOT B.DOK like 'ZO%';"
sql2 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and  B.DOK not like 'ZO%';"
sql3 = "select cast(A.POCETOBJ / (A.POCETOBJ + B.POCETOBJ) * 100 as INT)||' %' as POCETOBJ from(select '1' as AAA, cast(count(B.DOK) as float) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and  NOT B.DOK like 'ZO%') A left join (select '1' as AAA,cast(count(B.DOK) as float) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and  NOT B.DOK like 'ZO%') B on A.AAA=B.AAA;"
sql4 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where (B.STSZAK = 'E' or B.STSZAK = 'B' or B.STSZAK = 'K') and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.STS != 'U' and  NOT B.DOK like 'SO%'  and  NOT B.DOK like 'ZO%';"
sql5 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where (B.STSZAK = 'O' or B.STSZAK = 'V' or B.STSZAK = 'C') and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%';"
sql6 = "select cast(A.POCETOBJ / (A.POCETOBJ + B.POCETOBJ) * 100 as INT)||' %' as POCETOBJ from (select '1' as AAA, cast(count(B.DOK) as float) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where (B.STSZAK = 'E' or B.STSZAK = 'B' or B.STSZAK = 'K') and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.STS != 'U' and  NOT B.DOK like 'SO%') A left join (select '1' as AAA, cast(count(B.DOK) as float) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where (B.STSZAK = 'O' or B.STSZAK = 'V' or B.STSZAK = 'C') and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%') B on A.AAA = B.AAA;"
sql7 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'V' and B.STS != 'U' and G.KPO_SKU = 'REGION' and NOT B.DOK like 'SO%' and B.STSOK = 'S';"
sql8 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'B' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and  NOT B.DOK like 'SO%';"
sql9 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'K' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and  NOT B.DOK like 'SO%';"
sql10 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK = 'C' and B.STS != 'U' and G.KPO_SKU = 'REGION' and NOT B.DOK like 'SO%';"
sql11 = "select count(A.POCETOBJ) as POCET from (select distinct B.DOK as POCETOBJ from LOOBJP A inner join LOOBJ B on B.ID = A.IDLOOBJ left join KPO C on C.ID = B.IDKPOPRIJ left join KPROD D on D.ID = A.IDKPROD left join KPRODNR I on I.IDKPROD = D.ID where B.STSZAK = 'C' and B.STS != 'U'  and I.typPR = '1' and A.STSZAK = 'C' and NOT B.DOK like 'SO%') A;"
sql12 = "select count(A.POCETOBJ) as POCET from (select distinct B.DOK as POCETOBJ from LOOBJP A inner join LOOBJ B on B.ID = A.IDLOOBJ left join KPO C on C.ID = B.IDKPOPRIJ left join KPROD D on D.ID = A.IDKPROD left join KPRODNR I on I.IDKPROD = D.ID where B.STSZAK = 'C' and B.STS != 'U'  and I.typPR = '2' and A.STSZAK = 'C' and NOT B.DOK like 'SO%') A;"
sql13 = "select count(B.CIS) - count(A.CISMAJ) as pocetmaj from (select  distinct A.CISMAJ from  LSPRP A  inner join LSPR B on B.ID = A.IDLSPR  left join KPO C on C.ID = B.IDKPODOD  inner join LSSK D on D.ID = A.IDLSSK  inner join KPROD E on E.ID = D.IDKPROD where B.STS = 'B' and A.STS = 'B') A right join (select A.CIS from  KMAJPP A  left join KMAJP B on B.ID = A.IDKMAJP  left join ( SELECT    B.BARCODE, MIN(C.RAD) || '' || MIN(C.STLP) || '' || MIN(C.POSCHODIE) AS POZICIA  FROM    LSKPSKDP C     INNER JOIN LSKPSKDPP B ON B.IDLSKPSKDP = C.ID   GROUP BY      B.BARCODE) C on C.BARCODE = A.CIS  left join KPROD D on D.ID = B.IDKPROD where A.IDKMAJP = 41 and C.POZICIA = 'ZZ0104') B on B.CIS = A.CISMAJ;"
sql14 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and  NOT B.DOK like 'ZO%';"
sql15 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and I.KRT = 'DPD' and  NOT B.DOK like 'ZO%';"
sql16 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and I.KRT = 'GLS' and  NOT B.DOK like 'ZO%';" 
sql17 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and I.KRT like 'FED%' and  NOT B.DOK like 'ZO%';"
sql18 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and  NOT B.DOK like 'SO%' and I.KRT like 'UPS%' and  NOT B.DOK like 'ZO%';"
sql19 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK like 'S' and  NOT B.DOK like 'SO%' and NOT(upper(I.KRT like 'SPS' or I.KRT like 'GLS' OR I.KRT like 'DPD' or  I.KRT like 'FED%' or   I.KRT like 'UPS%' )) and  NOT B.DOK like 'ZO%';"
sql20 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.DOK like 'SO%'; "
sql21 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.DOK like 'SO%' and I.KRT = 'DPD';"
sql22 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.DOK like 'SO%' and I.KRT = 'GLS';"
sql23 ="select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.DOK like 'SO%' and I.KRT = 'FED';"
sql24 = "select count(B.DOK) as POCETOBJ from LOOBJ B left join KPO C on C.ID = B.IDKPOPRIJ left join KPOSKU E on C.ID = E.IDKPO left join KPO_SKU F on F.ID=E.IDKPO_SKU left join KPO_SKU G on G.ID=F.IDR left join KOS H on H.ID = B.IDKOSROZ left join KRT I on I.ID = B.IDKRT where B.STSZAK != 'E' and B.STS != 'U' and G.KPO_SKU = 'REGION' and B.DTROZP = current date and B.STSOK = 'S' and B.DOK like 'SO%' and NOT(I.KRT = 'SPS' or I.KRT = 'GLS' OR I.KRT = 'DPD');"

# --- Načítanie dát ---
df1 = load_data(sql1)
df2 = load_data(sql2)
df3 = load_data(sql3)
df4 = load_data(sql4)
df5 = load_data(sql5)
df6 = load_data(sql6)
df7 = load_data(sql7)
df8 = load_data(sql8)
df9 = load_data(sql9)
df10 = load_data(sql10)
df11 = load_data(sql11)
df12 = load_data(sql12)
df13 = load_data(sql13)
df14 = load_data(sql14)
df15 = load_data(sql15)
df16 = load_data(sql16)
df17 = load_data(sql17)
df18 = load_data(sql18)
df19 = load_data(sql19)
df20 = load_data(sql20)
df21 = load_data(sql21)
df22 = load_data(sql22)
df23 = load_data(sql23)
df24 = load_data(sql24)

# --- Funkcia na generovanie HTML tabuľky ---
def generate_table_html(df, table_name, top_px, left_px):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy SQL stĺpcov

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px;'>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table'>
            <thead><tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr></thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{val}</td>" for val in row]) + "</tr>"
    html += "</tbody></table></div>"
    return html
    
  # --- Funkcia na generovanie HTML tabuľky pre df3 so zelenou pri 100 % ---
def generate_table_html_df3(df, table_name, top_px, left_px):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy SQL stĺpcov

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px;'>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table'>
            <thead><tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr></thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            # Podmienka: ak hodnota = "100 %" -> zelená, inak modrá
            if str(val).strip() == "100 %":
                html += f"<td style='background-color: #28a745;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html
    
      # --- Funkcia na generovanie HTML tabuľky pre df4 so zelenou pri 100 % ---
def generate_table_html_df6(df, table_name, top_px, left_px):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy SQL stĺpcov

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px;'>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table'>
            <thead><tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr></thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            # Podmienka: ak hodnota = "100 %" -> zelená, inak modrá
            if str(val).strip() == "100 %":
                html += f"<td style='background-color: #28a745;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html
   
    # --- Funkcia na vytvorenie tlačidla PREBIEHA---
def generate_button_html(label, top_px, left_px, width_px=832, height_px=70):
    html = f"""
    <div style="
        position: absolute;
        top: {top_px}px;
        left: {left_px}px;
        width: {width_px}px;
        height: {height_px}px;
        background-color: #102B5D;   /* tmavomodré pozadie */
        color: white;                 /* biely text */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        font-weight: bold;
        border-radius: 0px;
        cursor: pointer;
        z-index: 1000;
    ">
        {label}
    </div>
    """
    return html
    
    
    
       # --- Funkcia na generovanie HTML tabuľky pre df10   
def generate_table_html_df10(df, table_name, top_px, left_px, width_px=552):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            try:
                num_val = float(val)
            except:
                num_val = None
            # >0 červené, inak pôvodná modrá
            if num_val is not None and num_val > 0:
                html += f"<td style='background-color: #D30000;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html


       # --- Funkcia na generovanie HTML tabuľky pre df11
def generate_table_html_df11(df, table_name, top_px, left_px, width_px=275):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            try:
                num_val = float(val)
            except:
                num_val = None
            # >0 červené, inak pôvodná modrá
            if num_val is not None and num_val > 0:
                html += f"<td style='background-color: #D30000;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html
    
           # --- Funkcia na generovanie HTML tabuľky pre df12
def generate_table_html_df12(df, table_name, top_px, left_px, width_px=275):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            try:
                num_val = float(val)
            except:
                num_val = None
            # >0 červené, inak pôvodná modrá
            if num_val is not None and num_val > 0:
                html += f"<td style='background-color: #D30000;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

       # --- Funkcia na generovanie HTML tabuľky pre df13
def generate_table_html_df13(df, table_name, top_px, left_px, width_px=552):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            try:
                num_val = float(val)
            except:
                num_val = None
            # >0 červené, inak pôvodná modrá
            if num_val is not None and num_val > 0:
                html += f"<td style='background-color: #D30000;'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html
    
        # --- Funkcia na vytvorenie tlačidla EXPEDICIA--
def generate_button_html2(label, top_px, left_px, width_px=832, height_px=70):
    html = f"""
    <div style="
        position: absolute;
        top: {top_px}px;
        left: {left_px}px;
        width: {width_px}px;
        height: {height_px}px;
        background-color: #102B5D;   /* tmavomodré pozadie */
        color: white;                 /* biely text */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        font-weight: bold;
        border-radius: 0px;
        cursor: pointer;
        z-index: 1000;
    ">
        {label}
    </div>
    """
    return html
    
    # --- Funkcia na generovanie HTML tabuľky pre df14
def generate_table_html_df14(df, table_name, top_px, left_px, width_px=832):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += "</tbody></table></div>"
    return html
    
    # --- HTML tabuľka pre df15 + text / obrázok v hlavičke
def generate_table_html_df15(
    df, table_name, top_px, left_px,
    width_px=161, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
        # --- HTML tabuľka pre df16+ text / obrázok v hlavičke
def generate_table_html_df16(
    df, table_name, top_px, left_px,
    width_px=161, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
            # --- HTML tabuľka pre df17+ text / obrázok v hlavičke
def generate_table_html_df17(
    df, table_name, top_px, left_px,
    width_px=161, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"

            # --- HTML tabuľka pre df18+ text / obrázok v hlavičke
def generate_table_html_df18(
    df, table_name, top_px, left_px,
    width_px=161, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"

            # --- HTML tabuľka pre df19
def generate_table_html_df19(
    df, table_name, top_px, left_px,
    width_px=172,
    header_bg="#e0e0e0",
    header_text_color="#3E424B",
    header_img_url=None,
    header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            color:{header_text_color};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            font-size:30px;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
        # --- Funkcia na generovanie HTML tabuľky pre df20
def generate_table_html_df20(df, table_name, top_px, left_px, width_px=832):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)  # skryť názvy stĺpcov

    html = f"""
    <div class='table-container' style='
        top:{top_px}px; 
        left:{left_px}px;
        width:{width_px}px;
        overflow:auto;
    '>
        <div class='table-title'>{table_name}</div>
        <table class='custom-table' style='
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        '>
            <thead>
                <tr>{''.join([f'<th>{col}</th>' for col in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += "</tbody></table></div>"
    return html
    
        # --- HTML tabuľka pre df21 + text / obrázok v hlavičke
def generate_table_html_df21(
    df, table_name, top_px, left_px,
    width_px=208, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
            # --- HTML tabuľka pre df22 + text / obrázok v hlavičke
def generate_table_html_df22(
    df, table_name, top_px, left_px,
    width_px=208, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
                # --- HTML tabuľka pre df23 + text / obrázok v hlavičke
def generate_table_html_df23(
    df, table_name, top_px, left_px,
    width_px=208, header_bg="#e0e0e0",
    header_img_url=None, header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"
    
            # --- HTML tabuľka pre df24
def generate_table_html_df24(
    df, table_name, top_px, left_px,
    width_px=196,
    header_bg="#e0e0e0",
    header_text_color="#3E424B",
    header_img_url=None,
    header_height=50
):
    df = df.dropna(axis=1, how='all')
    df.columns = [""] * len(df.columns)

    th_style = f"style='background:{header_bg};'" if header_bg else ""

    header_html = (
        f"<img src='{header_img_url}' "
        f"style='max-height:{header_height}px; max-width:100%; object-fit:contain;'>"
        if header_img_url else table_name
    )

    html = f"""
    <div class='table-container' style='top:{top_px}px; left:{left_px}px; width:{width_px}px; overflow:auto;'>
        <div class='table-title' style='
            background:{header_bg};
            color:{header_text_color};
            height:{header_height}px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            font-size:30px;
        '>
            {header_html}
        </div>
        <table class='custom-table' style='border-collapse:collapse;width:100%;table-layout:fixed;'>
            <thead>
                <tr>{''.join([f'<th {th_style}>{c}</th>' for c in df.columns])}</tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"

    return html + "</tbody></table></div>"




st.markdown(generate_table_html(df1, "OBJ dokončené", top_px=20, left_px=0), unsafe_allow_html=True)
st.markdown(generate_table_html(df2, "OBJ zostáva", top_px=4, left_px=279), unsafe_allow_html=True)
st.markdown(generate_table_html_df3(df3, "OBJ hotové", top_px=-12, left_px=558), unsafe_allow_html=True)
st.markdown(generate_table_html(df4, "Picker dokončené", top_px=90, left_px=0), unsafe_allow_html=True)
st.markdown(generate_table_html(df5, "Picker zostáva", top_px=74, left_px=279), unsafe_allow_html=True)
st.markdown(generate_table_html_df6(df6, "Picker hotové", top_px=58, left_px=558), unsafe_allow_html=True)
st.markdown(generate_button_html("PREBIEHA", top_px=-32, left_px=1150), unsafe_allow_html=True)
st.markdown(generate_table_html(df7, "Picker", top_px=26, left_px=1150), unsafe_allow_html=True)
st.markdown(generate_table_html(df8, "Balič", top_px=10, left_px=1429), unsafe_allow_html=True)
st.markdown(generate_table_html(df9, "Nezabalené", top_px=-6, left_px=1708), unsafe_allow_html=True)
st.markdown(generate_table_html_df10(df10, "Nevychystané OBJ", top_px=200, left_px=1292, width_px=552), unsafe_allow_html=True)
st.markdown(generate_table_html_df11(df11, "Čaká doložiť", top_px=302, left_px=1292, width_px=275), unsafe_allow_html=True)
st.markdown(generate_table_html_df12(df12, "Čaká vyrobiť", top_px=286, left_px=1571, width_px=275), unsafe_allow_html=True)
st.markdown(generate_table_html_df13(df13, "Počet nezaskladnených MAJ", top_px=450, left_px=1292, width_px=552), unsafe_allow_html=True)
st.markdown(generate_button_html2("EPEDÍCIA", top_px=80, left_px=0), unsafe_allow_html=True)
st.markdown(generate_table_html_df14(df14, "Spolu OBJ", top_px=138, left_px=0, width_px=832), unsafe_allow_html=True)
st.markdown(generate_table_html_df15(df15, table_name="", top_px=240, left_px=0, header_img_url="https://upload.wikimedia.org/wikipedia/commons/4/4c/DPD_logo%28red%292015.png"), unsafe_allow_html=True)
st.markdown(generate_table_html_df16(df16, table_name="", top_px=224, left_px=165, header_img_url="https://upload.wikimedia.org/wikipedia/de/e/ea/General_Logistics_Systems_logo.svg"), unsafe_allow_html=True)
st.markdown(generate_table_html_df17(df17, table_name="", top_px=208, left_px=330, header_img_url="https://freepngimg.com/thumb/logo/142493-logo-picture-fedex-free-hd-image.png"), unsafe_allow_html=True)
st.markdown(generate_table_html_df18(df18, table_name="", top_px=192, left_px=495, header_img_url="https://upload.wikimedia.org/wikipedia/commons/6/6b/United_Parcel_Service_logo_2014.svg"), unsafe_allow_html=True)
st.markdown(generate_table_html_df19(df19,"NEZ", top_px=176, left_px=660, width_px=172, header_bg="#E0E0E0",header_text_color="#3E424B"), unsafe_allow_html=True)
st.markdown(generate_table_html_df20(df20, "Spolu Servis", top_px=330, left_px=0, width_px=832), unsafe_allow_html=True)
st.markdown(generate_table_html_df21(df21, table_name="", top_px=433, left_px=0, header_img_url="https://upload.wikimedia.org/wikipedia/commons/4/4c/DPD_logo%28red%292015.png"), unsafe_allow_html=True)
st.markdown(generate_table_html_df22(df22, table_name="", top_px=417, left_px=212, header_img_url="https://upload.wikimedia.org/wikipedia/de/e/ea/General_Logistics_Systems_logo.svg"), unsafe_allow_html=True)
st.markdown(generate_table_html_df23(df23, table_name="", top_px=401, left_px=424, header_img_url="https://freepngimg.com/thumb/logo/142493-logo-picture-fedex-free-hd-image.png"), unsafe_allow_html=True)
st.markdown(generate_table_html_df24(df24,"NEZ", top_px=385, left_px=636, width_px=196, header_bg="#E0E0E0",header_text_color="#3E424B"), unsafe_allow_html=True)
