from app import app, api
from web.api.admin.views import ns as admin_ns
from web.api.upload_pdf.views import ns as pdf_nsd

# Add the namespace to the API
api.add_namespace(admin_ns)
api.add_namespace(pdf_nsd)

if __name__ == '__main__':
    app.run(debug=True)
