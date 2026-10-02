import json

with open('semana_40_master.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Contar apariciones de Sal de mar mineral de Colima
print("Ocurrencias de 'Sal de mar mineral de Colima':", text.count("Sal de mar mineral de Colima"))

# Reemplazar
new_text = text.replace("Sal de mar mineral de Colima", "Sal de mar")

with open('semana_40_master.json', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Reemplazo completado con éxito en semana_40_master.json")
