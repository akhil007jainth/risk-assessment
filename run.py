from app import app, api
from web.api.admin.views import ns as admin_ns
from web.api.upload_pdf.views import ns as pdf_nsd
from web.api.scores.views import ns as set_question

# Add the namespace to the API
api.add_namespace(admin_ns)
api.add_namespace(pdf_nsd)
api.add_namespace(set_question)

if __name__ == '__main__':
    app.run( host="0.0.0.0")
