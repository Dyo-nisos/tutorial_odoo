{
    'name': "real_estate",
    'version': '17.0.0.0.1',
    'depends': ['base', 'account'],
    'author': "Author Name",
    'category': 'Administrator',
    'description': """
    Description text
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'security/ir.model.access.csv',
        'views/estate_property_custom_views.xml',
    ],
    # data files containing optionally loaded demonstration data
}
