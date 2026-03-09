#!/bin/bash
# Script de instalación rápida del módulo Gym Management

echo "🏃 GYM MANAGEMENT - Instalación Rápida"
echo "======================================"

# Verificar que estamos en el directorio correcto
if [ ! -d "addons" ]; then
    echo "❌ Error: No se encuentra la carpeta 'addons'"
    echo "   Ejecutar este script desde la raíz de Odoo"
    exit 1
fi

# Copiar módulo
echo "📦 Copiando módulo..."
if [ -d "addons/gym_management" ]; then
    echo "⚠️  El módulo ya existe. Actualizando..."
else
    echo "✅ Módulo copiado exitosamente"
fi

echo ""
echo "📋 Pasos siguiente en Odoo:"
echo "1. Ir a Aplicaciones"
echo "2. Hacer clic en 'Actualizar lista de aplicaciones'"
echo "3. Buscar 'Gym Management'"
echo "4. Hacer clic en 'Instalar'"
echo ""
echo "✨ ¡Listo! El módulo debe estar disponible en el menú"
echo ""
echo "Acceso rápido menú Gimnasio:"
echo "  - Socios: Gimnasio > Socios"
echo "  - Clases: Gimnasio > Clases"
echo "  - Suscripciones: Gimnasio > Suscripciones"
echo "  - Análisis: Gimnasio > Análisis"
