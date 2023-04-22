from flask import Blueprint

managers = Blueprint('managers',__name__)


import base64

@managers.route("/manager")
def manager():
    # expense = Expense.query.filter_by(managerid='man001').first()  # Retrieve the first expense record
    # image_data = expense.picture
    
    # mime_type = mimetypes.guess_type("image.jpg")[0]  # Replace "image.jpg" with the actual file name
    
    # return Response(image_data, mimetype=mime_type)
    pass