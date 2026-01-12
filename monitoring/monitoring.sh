if ! curl -f http://localhost:5000/health; then
    echo "ALERT: Application DOWN"
    exit 1
fi
