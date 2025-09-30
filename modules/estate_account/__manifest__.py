{
    'name': "estate_account",
    'version': '17.0.0.0.1',
    'depends': ['estate', 'account'],
    'author': "Author Name",
    'category': 'Administrator',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        # 'security/ir.model.access.csv', # No tenemos model para un csv security (nuevo)
        'views/estate_property_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
}