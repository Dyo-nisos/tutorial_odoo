{
    'name': "invoice_inherit",
    'version': '17.0.0.0.1',
    'depends': ['base', 'account'],
    'author': "Author Name",
    'category': 'Administrator',
    'description': """
    Description text
    """,
    'installable': True,
    'application': False,
    # data files always loaded at installation
    'data': [
        'security/group_edit_so_invoice_lines.xml',
        'views/account_move_lines_view.xml',
    ],
    # data files containing optionally loaded demonstration data
}
