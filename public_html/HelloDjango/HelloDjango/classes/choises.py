class Section():
    TYPES = (
        ('Carrier', 'Плитоносцы и доп.оснащение'),
        ('Chestrigs', 'Нагрудники'),
        ('BeltsTraps', 'Пояса и лямки'),
        ('Pouches', 'Подсумки'),
        ('Bags', 'Рюкзаки и сумки'),
        ('Armor', 'Бронеэлементы'),
        ('Other', 'Прочее')
    )
    
    SUBSECTION = {
        'Carrier' : (
            ('Plate_presets', 'Готовые комплекты', '/media/static/images/subcategories/PLATE.jpg'),
            ('Plate_parts', 'Составные части', '/media/static/images/subcategories/Plate_parts.JPG'),
            ('Plate_additional', 'Дополнительное оснащение', '/media/static/images/subcategories/Dop.JPG'),
        ),
        'Chestrigs' : (
            ('Chest_presets', 'Готовые комплекты', '/media/static/images/subcategories/ifak.jpg'),
            ('Chest_parts', 'Составные части', '/media/static/images/subcategories/gran.jpg'),    
         ),
        'Pouches' : (
            ('Medical', 'Медицинские подсумки', '/media/static/images/subcategories/ifak.jpg'),
            ('Grenades_equipment', 'Подсумки под гранаты и спецсредства', '/media/static/images/subcategories/gran.jpg'),
            ('Magazines_ribbons', 'Подсумки под магазины, ленты, короба, патроны', '/media/static/images/subcategories/mags.jpg'),
            ('Utility', 'Утилитарные подсумки', '/media/static/images/subcategories/utility.jpg'),
            ('Other_pouch','Прочие подсумки', '/media/static/images/subcategories/other_pouches.jpg')
        ),
        'Other' : (
            ('Weapon_slings', 'Оружейные ремни', '/media/static/images/subcategories/slings.jpg'),
            ('Holsters', 'Кобуры', '/media/static/images/subcategories/holsters.jpg'),
            ('Backmat', 'Сидушки и коврики', '/media/static/images/subcategories/SIT.jpg'),
            ('Covers', 'Чехлы на шлема', '/media/static/images/subcategories/covers.jpg'),
            ('Patches','Патчи и повязки', '/media/static/images/subcategories/patches.jpg')
        )
    }
    

    STATE_CHOICES = [
        ('INACTIVE', 'Неактивно'),
        ('ACTIVE', 'Активно'),
        ('ACCEPTED', 'Подтверждено'),
        ('PROCESSED', 'Обработано'),
        ('DECLINED', 'Отклонено'),
    ]

    POST_CHOICES = (
        ('ARTICLE', 'Статья'),
        ('NEWS', 'Новость или Акция')
    )
