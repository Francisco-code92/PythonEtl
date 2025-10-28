import os
import pandas as pd

# 1. Cargar Datos
datos = pd.read_csv("ventas.csv")

# Normalizar datos
for col in ["entity", "country", "currency"]:
    datos[col] = datos[col].astype(str).str.strip().str.upper()

# 2. Convertir a USD
fx_to_usd = {"USD": 1.0, "COP": 0.00026, "PEN": 0.27}
datos["fx"] = datos["currency"].map(fx_to_usd)

datos["net_usd"] = (datos["net_amount"] * datos["fx"]).round(2)
datos["tax_usd"] = (datos["tax_amount"] * datos["fx"]).round(2)

# 3. Agregar por "country"
res = (
    datos.groupby("country", as_index=False)
    .agg(net_usd=("net_usd", "sum"),
         tax_usd=("tax_usd", "sum"))
    .sort_values("country")
)

# 4. Exportar resumen_pais.csv
os.makedirs("output", exist_ok=True)
out_path = os.path.join("output", "resumen_pais.csv")
res.to_csv(out_path, index=False)

# 5. Log Simple
total_cols = len(datos)
dis_countries = datos["country"].nunique()
total_net_usd = res["net_usd"].sum()
total_tax_usd = res["tax_usd"].sum()

print("----------LOG ETL VENTAS---------")
print(f"Filas contadas: {total_cols}")
print(f"Paises: {dis_countries}")
print(f"NET USD total: {total_net_usd}")
print(f"TAX USD total: {total_tax_usd}")
print(f"Archivo generado: {out_path}")
print("---------LOG ETL VENTAS---------")
