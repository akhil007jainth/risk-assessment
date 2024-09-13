from app import app, api
from web.api.admin.views import ns

# Add the namespace to the API
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug=True)
