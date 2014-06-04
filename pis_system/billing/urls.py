from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from billing.views import(
	student,
	get_bill,
	get_student,
	get_suggestions,
	bill_student,
  transact,
  transact_one,
  others,
  add_bill,
  get_history_transaction,
  get_item_history_transaction
	)
  
urlpatterns = patterns('',
  url(r'^get_history?', get_history_transaction),
  url(r'^getitemhistory?', get_item_history_transaction),
  url(r'^getbill?', get_bill),
  url(r'^getstudent?', get_student),
  url(r'^search_item?', get_suggestions),
  url(r'^bill_student?', bill_student),
  url(r'^student/transact$', transact),
  url(r'^student$', student),
  url(r'^others/add_bill$', add_bill),
  url(r'^transact_one$', transact_one),
  url(r'^others$', others),
  url(r'^$', student)
)