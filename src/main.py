from forms.form_master import FormMasterDesign
from database.dboperations import DBOps

database = DBOps()
type_ids, names = database.item_types_query()

app = FormMasterDesign(names)

app.mainloop()