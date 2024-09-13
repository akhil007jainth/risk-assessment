from app import app, api
from web.api.user.views import ns

# Add the namespace to the API
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
