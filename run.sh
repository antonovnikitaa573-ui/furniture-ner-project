echo "========================================"
echo "  Мебельный экстрактор товаров"
echo "========================================"
echo ""
echo "1 - Запустить main.py (один URL)"
echo "2 - Запустить database_builder.py (база из CSV)"
echo "3 - Запустить web_app.py (веб-интерфейс)"
echo ""
read -p "Выберите (1-3): " choice

case $choice in
    1)
        python scripts/main.py
        ;;
    2)
        python scripts/database_builder.py
        ;;
    3)
        python scripts/web_app.py
        ;;
    *)
        echo "Неверный выбор"
        ;;
esac