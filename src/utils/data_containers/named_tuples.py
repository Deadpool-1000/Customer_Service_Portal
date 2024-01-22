from collections import namedtuple

Employee = namedtuple('Employee', (
    'e_id',
    'name',
    'email',
    'address',
    'phn_num',
    'dept_name',
    'dept_id',
    'designation'
))

Ticket = namedtuple('Ticket', (
    't_id',
    'd_id',
    'c_id',
    'repr_id',
    'title',
    'description',
    'status',
    'cust_feedback',
    'created_on',
    'message'
))

Customer = namedtuple('Customer',(
    'c_id',
    'name',
    'email',
    'phn_num',
    'address'
))

Feedback = namedtuple('Feedback', (
    'f_id',
    't_id',
    'desc',
    'stars'
))
