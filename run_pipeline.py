import subprocess
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

scripts = [
    os.path.join(base_dir, "scripts", "ingestao.py"),
    os.path.join(base_dir, "scripts", "silver.py"),
    os.path.join(base_dir, "scripts", "gold.py"),
]

print("=" * 50)
print("EXECUTANDO PIPELINE MEDALHÃO")
print("=" * 50)

for script in scripts:
    print(f"\nRodando {os.path.basename(script)}...\n")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Erro ao executar {os.path.basename(script)}. Pipeline interrompido.")
        sys.exit(1)

print("\n" + "=" * 50)
print("PIPELINE FINALIZADO COM SUCESSO!")
print("=" * 50)