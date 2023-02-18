from app import app

if __name__ == '__main__':
    # notre méthode principal (main) pour lancer l'app
    app.run(host="localhost", port=8001, debug=True)