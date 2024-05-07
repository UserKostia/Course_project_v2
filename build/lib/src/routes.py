from views.sign_up import sign_up
from views.sign_in import sign_in
from views.index_view import index_view
from views.patients_view import patiens_view
from views.settings_view import settings_view
from views.doc_records import doc_records_view
from views.add_new_doc_view import add_new_doc_view
from views.add_patient_rec_view import add_new_patient_view
from utils.router import Router, DataStrategyEnum


router = Router(DataStrategyEnum.QUERY)

router.routes = {
    "/": sign_in,
    "/sign_up": sign_up,
    "/main": index_view,
    "/doc_rec": doc_records_view,
    "/patient": patiens_view,
    "/settings": settings_view,
    "/add_doc": add_new_doc_view,
    "/add_pnt": add_new_patient_view,
}
