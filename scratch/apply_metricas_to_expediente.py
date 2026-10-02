import sys, os
sys.stdout.reconfigure(encoding='utf-8')

with open('expediente_completo_semana_40.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 3.1 categories for oils and butters
content = content.replace(
    "| **Aceite de ajonjolí tostado** | 30 | ml | Lácteos y Grasas Saludables |",
    "| **Aceite de ajonjolí tostado** | 30 | ml | Grasas y Aceites Saludables |"
)
content = content.replace(
    "| **Aceite de oliva extra virgen (VEVO)** | 750 | ml | Lácteos y Grasas Saludables |",
    "| **Aceite de oliva extra virgen (VEVO)** | 750 | ml | Grasas y Aceites Saludables |"
)
content = content.replace(
    "| **Mantequilla clarificada (Ghee)** | 132 | g | Lácteos y Grasas Saludables |",
    "| **Mantequilla clarificada (Ghee)** | 132 | g | Grasas y Aceites Saludables |"
)
content = content.replace(
    "| **Mantequilla de pastoreo artesanal** | 960 | g | Lácteos y Grasas Saludables |",
    "| **Mantequilla de pastoreo artesanal** | 960 | g | Grasas y Aceites Saludables |"
)

# 2. Read Section 4 metricas
with open('scratch/metricas_section.md', 'r', encoding='utf-8') as f:
    metricas_md = f.read()

# 3. Replace ## 4. Dictamen de Conformidad Bioquímica y Operativa with Section 4 (Metricas) and Section 5 (Dictamen)
old_sec4_marker = "## 4. Dictamen de Conformidad Bioquímica y Operativa"
new_sections = metricas_md + "\n\n---\n\n## 5. Dictamen de Conformidad Bioquímica y Operativa"

if old_sec4_marker in content:
    content = content.replace(old_sec4_marker, new_sections)
    print("Successfully replaced section 4 and added metricas!")
else:
    print("Error: old_sec4_marker not found in content!")

with open('expediente_completo_semana_40.md', 'w', encoding='utf-8') as f:
    f.write(content)

# Also update the artifact file
artifact_path = r"C:\Users\andre\.gemini\antigravity\brain\77a3e1ca-fab2-4f79-b956-c9dd52a8791d\expediente_completo_semana_40.md"
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated expediente_completo_semana_40.md (size: {len(content)} chars)")
