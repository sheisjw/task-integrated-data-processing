from routes import app
import os

port = int(os.environ.get('PORT', 3000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True, threaded=True)
